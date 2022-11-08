import json

import grpc
import redis
import simulation_pb2
import simulation_pb2_grpc


def run():
    db = redis.StrictRedis("localhost", 6379, charset="utf-8", decode_responses=True)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)

        stub = simulation_pb2_grpc.SimulationStub(channel)
        stub.Stop(simulation_pb2.Empty())

        stub = simulation_pb2_grpc.SimulationStub(channel)
        stub.CreateBody(
            simulation_pb2.CreateBodyRequest(
                id=1,
                mass=1.989e30,
                position={"x": 0, "y": 0},
                velocity={"x": 0, "y": 0},
            )
        )
        stub.CreateBody(
            simulation_pb2.CreateBodyRequest(
                id=2,
                mass=5.972e24,
                position={"x": 149.600e9, "y": 0},
                velocity={"x": 0, "y": 30.000e3},
            )
        )

        stub = simulation_pb2_grpc.SimulationStub(channel)
        stub.Start(simulation_pb2.Empty())

    sub = db.pubsub()
    sub.subscribe("bodies")

    for message in sub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            spos = data[0]["position"]
            epos = data[1]["position"]
            print(
                f"Sun: X:{spos['x']:.4f} Y:{spos['y']:.4f}",
                f"Earth: X:{epos['x']:.4f} Y:{epos['y']:.4f}",
            )


run()
