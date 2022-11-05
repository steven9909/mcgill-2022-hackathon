from fastapi import APIRouter


post_route = APIRouter()

@post_route.post("/simulations/")
async def post_simulations(sim_data):
    return {"sim": "created"}

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

@post_route.post("/simulations/{sim_id}/planets")
async def post_simulations_planets(sim_id, planet_data):
    return {"sim_id": sim_id,
            "planets": "created"}
