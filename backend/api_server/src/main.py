from database.redis import RedisDb
from fastapi import FastAPI, WebSocket
from routes.get import get_route
from routes.post import post_route
from routes.delete import delete_route
from routes.put import put_route
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        datas = redis.get_bodies([-1, 1, 2, 3])
       
        await websocket.send_json([{
            "bodyId": i,
            "positionX": data[0].decode('utf8'),
            "positionY": data[1].decode('utf8'),
            "velocityX": data[2].decode('utf8'),
            "velocityY": data[3].decode('utf8'),
        } for i, data in enumerate(datas)])

