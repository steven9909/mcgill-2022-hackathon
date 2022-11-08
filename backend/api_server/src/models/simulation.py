from datetime import datetime
from typing import List, Optional

from database.body import (
    create_body,
    delete_body,
    fetch_bodies,
    fetch_body,
    update_body,
)
from models.body import Body, Vec2
from pydantic import BaseModel


class Simulation(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    def create_body(
        self,
        mass: float,
        initial_position: Vec2,
        initial_velocity: Vec2,
        model_path: str,
    ) -> Body:

        return create_body(
            self.id, mass, initial_position, initial_velocity, model_path
        )

    def fetch_body(self, id: int) -> Body:

        return fetch_body(id, self.id)

    def fetch_bodies(self) -> List[Body]:

        return fetch_bodies(self.id)

    def update_body(
        self,
        id: int,
        mass: Optional[float] = None,
        initial_position: Optional[Vec2] = None,
        initial_velocity: Optional[Vec2] = None,
        model_path: Optional[str] = None,
    ) -> Body:

        return update_body(
            id, self.id, mass, initial_position, initial_velocity, model_path
        )

    def delete_body(self, id: int):

        delete_body(id, self.id)
