from fastapi import APIRouter
from database.simulation import fetch_simulations, fetch_simulation


get_route = APIRouter()

@get_route.get("/simulations")
async def get_simulations():
    sims = fetch_simulations()
    return { "simulations": [x.json() for x in sims]}

@get_route.get("/simulations/{sim_id}")
async def get_simultaions(sim_id):
    sim = fetch_simulation(sim_id)
    return {"simulation": sim}

@get_route.get("/simulations/{sim_id}/body")
async def get_simultaions_body(sim_id):
    sim = fetch_simulation(sim_id)
    bodies = sim.fetch_bodies()
    return {"bodies": [x.json() for x in bodies]}

@get_route.get("/simulations/{sim_id}/body/{body_id}")
async def get_simultaions_body(sim_id, body_id):
    sim = fetch_simulation(sim_id)
    body = sim.fetch_body(body_id)
    return {"body": body}