from models.vec import (Vec2)
from pydantic import BaseModel

class Body(BaseModel):
    mass: float
    initial_position: Vec2
    initial_velocity: Vec2
    model_path: str