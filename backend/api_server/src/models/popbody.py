from models.vec import Vec2
from pydantic import BaseModel


class PopulationBody(BaseModel):
    init_position: Vec2
    end_positon: Vec2
