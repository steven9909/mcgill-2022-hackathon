from fastapi import APIRouter
from database.simulation import fetch_simulation, delete_simulation



delete_route = APIRouter()

@delete_route.delete("/simulations/{sim_id}")
async def delete_simulations_planets(sim_id):
    delete_simulation(sim_id)
    return {"status" : "sim deleted"}

@delete_route.delete("/simulations/{sim_id}/body/{planet_id}")
async def delete_simulations_planets(sim_id, body_id):
    sim = fetch_simulation(sim_id)
    sim.delete_body(body_id)
    return {"status" : "sim deleted"}