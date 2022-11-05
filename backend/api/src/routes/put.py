from fastapi import APIRouter


put_route = APIRouter()

@put_route.put("/simulations/{sim_id}/planets/{planet_id}")
async def put_simulations_planets(sim_id, planet_id):
    return {"sim_id": sim_id,
            "planet_id": planet_id,
            "planet": "updated"}