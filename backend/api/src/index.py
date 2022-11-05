from fastapi import FastAPI

app = FastAPI()

###########################################################################
# GET
###########################################################################


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/simulations")
async def get_simulations():
    return {"sim" : "Simulation"}

@app.get("/simulations/{sim_id}")
async def get_simultaions(sim_id):
    return {"sim_id": sim_id}

@app.get("/simulations/{sim_id}/planets")
async def get_simultaions_planets(sim_id):
    return {"sim_id": sim_id}

@app.get("/simulations/{sim_id}/planets/{planet_id}")
async def get_simultaions_planets(sim_id, planet_id):
    return {"sim_id": sim_id,
            "planet_id": planet_id}

###########################################################################
# POST
###########################################################################

@app.post("/simulations/{sim_id}")
async def post_simulations(sim_id):
    return {"sim_id": sim_id}

@app.post("/simulations/{sim_id}/start")
async def post_simulations_start(sim_id):
    return {"sim_id": sim_id}

@app.post("/simulations/{sim_id}/pause")
async def post_simulations_pause(sim_id):
    return {"sim_id": sim_id}

@app.post("/simulations/{sim_id}/stop")
async def post_simulations_stop(sim_id):
    return {"sim_id": sim_id}

@app.post("/simulations/{sim_id}/planets")
async def post_simulations_planets(sim_id):
    return {"sim_id": sim_id}

###########################################################################
# DELETE
###########################################################################

@app.delete("/simulations/{sim_id}/planets/{planet_id}")
async def delete_simulations_planets(sim_id, planet_id):
    return {"sim_id": sim_id,
        "planet_id": planet_id}

###########################################################################
# PUT
###########################################################################

@app.put("/simulations/{sim_id}/planets/{planet_id}")
async def put_simulations_planets(sim_id, planet_id):
    return {"sim_id": sim_id,
        "planet_id": planet_id}