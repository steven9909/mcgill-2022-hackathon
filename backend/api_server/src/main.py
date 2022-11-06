from database.redis import RedisDb
import time

'''
app = FastAPI()

app.include_router(get_route)
app.include_router(post_route)
app.include_router(delete_route)
app.include_router(put_route)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.websocket("/ws/1")
async def websocket_endpoint(websocket: WebSocket):
    redis = RedisDb()
    await websocket.accept()
    while True:
        print(redis.get_bodies([1, 2, 3]))
        await websocket.send_json()
'''
redis = RedisDb()
while True:
    print(redis.get_bodies([1, 2]))
    time.sleep(1)