import os

import grpc
import simulation_pb2_grpc
import simulation_pb2
from models.body import Body
from database.simulation import fetch_simulations, fetch_simulation, create_simulation

from fastapi import APIRouter

post_route = APIRouter()


@post_route.post("/simulations/")
async def post_simulations(sim_name: str):
    ret_val = create_simulation(sim_name)
    return ret_val

@post_route.post("/simulations/{sim_id}/body")
async def post_simulations_body(sim_id, body: Body):
    sim = fetch_simulation(sim_id)
    new_body = sim.create_body(body.mass,body.initial_position,body.initial_velocity,body.model_path)
    return {"body": new_body}


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
