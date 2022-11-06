from fastapi import APIRouter
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
    new_body = sim.update_body(body_id, body.mass, body.initial_position, body.initial_velocity, body.model_path)
    return {"body": new_body}
