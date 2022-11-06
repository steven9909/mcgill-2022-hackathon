from fastapi import APIRouter
import grpc
import simulation_pb2_grpc
import simulation_pb2
from models.body import Body
from database.simulation import fetch_simulation, update_simulation


put_route = APIRouter()


@put_route.put("/simulations/{sim_id}")
async def put_simulations_bodys(sim_id, sim_name: str):
    sim = update_simulation(sim_id, sim_name)
    return {"simulation": sim}


@put_route.put("/simulations/{sim_id}/body/{body_id}")
async def put_simulations_bodys(sim_id, body_id, body: Body):
    sim = fetch_simulation(sim_id)
    new_body = sim.update_body(
        body_id,
        body.mass,
        body.initial_position,
        body.initial_velocity,
        body.model_path,
    )

    with grpc.insecure_channel("localhost:50051") as channel:
        stub = simulation_pb2_grpc.SimulationStub(channel)
        assert stub.UpdateBody(
            simulation_pb2.UpdateBodyParam(
                id=new_body.id,
                p_x=new_body.initial_position.x,
                p_y=new_body.initial_position.y,
                v_x=new_body.initial_velocity.x,
                v_y=new_body.initial_velocity.y,
            )
        )

    return {"body": new_body}
