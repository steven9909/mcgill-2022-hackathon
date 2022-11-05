from fastapi import APIRouter


delete_route = APIRouter()

@delete_route.delete("/simulations/{sim_id}/planets/{planet_id}")
async def delete_simulations_planets(sim_id, planet_id):
    return {"sim_id": sim_id, 
            "planet_id": planet_id,
            "planet": "deleted"}