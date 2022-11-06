from fastapi import APIRouter
import grpc
import simulation_pb2_grpc
import simulation_pb2
from database.simulation import fetch_simulation, delete_simulation


delete_route = APIRouter()


@delete_route.delete("/simulations/{sim_id}")
async def delete_simulations_planets(sim_id):
    delete_simulation(sim_id)
    return {"status": "sim deleted"}


@delete_route.delete("/simulations/{sim_id}/body/{planet_id}")
async def delete_simulations_planets(sim_id, body_id):
    sim = fetch_simulation(sim_id)
    sim.delete_body(body_id)

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.DeleteBody(
            simulation_pb2.DeleteBodyParam(
                id=body_id,
            )
        )
    return {"status": "sim deleted"}
