from fastapi import FastAPI
from routes.get import get_route
from routes.post import post_route
from routes.delete import delete_route
from routes.put import put_route

app = FastAPI()

app.include_router(get_route)
app.include_router(post_route)
app.include_router(delete_route)
app.include_router(post_route)

@app.get("/")
async def root():
    return {"message": "Hello World"}