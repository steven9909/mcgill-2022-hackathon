from datetime import datetime

from pydantic import BaseModel


class Vec2(BaseModel):
    x: float
    y: float


class Body(BaseModel):
    id: int
    simulation_id: int
    mass: float
    initial_position: Vec2
    initial_velocity: Vec2
    model_path: str
    created_at: datetime
    updated_at: datetime
