import os

import grpc
import simulation_pb2_grpc
import simulation_pb2
from fastapi import APIRouter

post_route = APIRouter()


@post_route.post("/simulations/")
async def post_simulations(sim_data):
    return {"sim": "created"}


@post_route.post("/simulations/{sim_id}/bodys")
async def post_simulations_bodys(sim_id, body_data):
    return {"sim_id": sim_id, "bodies": "created"}


@post_route.post("/simulator/start")
async def post_simulation_start():
    with grpc.insecure_channel(os.environ.get("SIM_SERVER_URL")) as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.Start(simulation_pb2.EmptyParam())


@post_route.post("/simulator/pause")
async def post_simulation_pause():
    with grpc.insecure_channel(os.environ.get("SIM_SERVER_URL")) as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.Pause(simulation_pb2.EmptyParam())


@post_route.post("/simulator/stop")
async def post_simulation_stop():
    with grpc.insecure_channel(os.environ.get("SIM_SERVER_URL")) as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.Stop(simulation_pb2.EmptyParam())
