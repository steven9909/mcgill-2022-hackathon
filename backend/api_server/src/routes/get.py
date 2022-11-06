from fastapi import APIRouter


get_route = APIRouter()

@get_route.get("/simulations")
async def get_simulations():
    return {"sim" : "Simulation"}

@get_route.get("/simulations/{sim_id}")
async def get_simultaions(sim_id):
    return {"sim_id": sim_id}

@get_route.get("/simulations/{sim_id}/planets")
async def get_simultaions_planets(sim_id):
    return {"sim_id": sim_id,
            "planets": "planets"}

@get_route.get("/simulations/{sim_id}/planets/{planet_id}")
async def get_simultaions_planets(sim_id, planet_id):
    return {"sim_id": sim_id,
            "planet_id": planet_id}