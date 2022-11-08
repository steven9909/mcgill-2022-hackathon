import json
import os

import redis
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(get_route)
# app.include_router(post_route)
# app.include_router(delete_route)
# app.include_router(put_route)

db = redis.StrictRedis(
    *os.environ.get("REDIS_URL").split(":"), charset="utf-8", decode_responses=True
)


@app.websocket("/bodies")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    sub = db.pubsub()
    sub.subscribe("bodies")

    for message in sub.listen():
        if message["type"] != "message":
            continue

        await websocket.send_json(json.loads(message["data"]))


if __name__ == "__main__":
    host, port = os.environ.get("API_SERVER:URL").split(":")
    uvicorn.run("main:app", host=host, port=port)
