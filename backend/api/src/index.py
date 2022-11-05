from fastapi import FastAPI
from get import get_route
from post import post_route
from delete import delete_route
from put import put_route

app = FastAPI()

app.include_router(get_route)
app.include_router(post_route)
app.include_router(delete_route)
app.include_router(post_route)

@app.get("/")
async def root():
    return {"message": "Hello World"}