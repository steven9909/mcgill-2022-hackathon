from database.redis import RedisDb
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from routes.get import get_route
from routes.post import post_route
from routes.delete import delete_route
from routes.put import put_route
from database.simulation import fetch_simulation
from fastapi.middleware.cors import CORSMiddleware
import grpc
import simulation_pb2_grpc
import simulation_pb2

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://10.0.0.239:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_route)
app.include_router(post_route)
app.include_router(delete_route)
app.include_router(put_route)

redis = RedisDb()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)


manager = ConnectionManager()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.Start(simulation_pb2.EmptyParam())

    # with grpc.insecure_channel("localhost:50051") as channel:
    #     stub = simulation_pb2_grpc.SimulationStub(channel)
    #     assert stub.InitializePopulation(
    #         simulation_pb2.CreatePopulationParam(
    #             start_x=1e11,
    #             start_y=1e11,
    #             end_x=0,
    #             end_y=0,
    #         )
    #     )

    sim = fetch_simulation(6)
    bodies = sim.fetch_bodies()
    body_ids = [x.id for x in bodies]
    # for i in range(2, 27):
    #     body_ids.append(-i)

    for x in bodies:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = simulation_pb2_grpc.SimulationStub(channel)
            assert stub.CreateBody(
                simulation_pb2.CreateBodyParam(
                    id=x.id,
                    mass=x.mass,
                    p_x=x.initial_position.x,
                    p_y=x.initial_position.y,
                    v_x=x.initial_velocity.x,
                    v_y=x.initial_velocity.y,
                )
            )

    try:
        while True:
            datas = redis.get_bodies(body_ids)

            await websocket.send_json(
                [
                    {
                        "bodyId": i,
                        "positionX": data[0].decode("utf8"),
                        "positionY": data[1].decode("utf8"),
                        "velocityX": data[2].decode("utf8"),
                        "velocityY": data[3].decode("utf8"),
                    }
                    for i, data in enumerate(datas)
                ]
            )

    except Exception:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = simulation_pb2_grpc.SimulationStub(channel)
            assert stub.Stop(simulation_pb2.EmptyParam())
