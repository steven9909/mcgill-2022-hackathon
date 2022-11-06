from fastapi import APIRouter

from database.simulation import Simulation, create_simulation, fetch_simulation, fetch_simulations
from models.body import Body

post_route = APIRouter()

@post_route.post("/simulations/")
async def post_simulations(sim_name: str):
    ret_val = create_simulation(sim_name)
    return ret_val

@post_route.post("/simulations/{sim_id}/start")
async def post_simulations_start(sim_id):
    return {"sim": sim_id,
            "sim": "started"}

@post_route.post("/simulations/{sim_id}/pause")
async def post_simulations_pause(sim_id):
    return {"sim": sim_id,
            "sim": "paused"}

@post_route.post("/simulations/{sim_id}/stop")
async def post_simulations_stop(sim_id):
    return {"sim": sim_id,
            "sim": "stopeed"}

@post_route.post("/simulations/{sim_id}/body")
async def post_simulations_body(sim_id, body: Body):
    sim = fetch_simulation(sim_id)
    new_body = sim.create_body(body.mass,body.initial_position,body.initial_velocity,body.model_path)
    return {"body": new_body}
