from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from database.body import (
    Body,
    Vec2,
    create_body,
    delete_body,
    fetch_bodies,
    fetch_body,
    update_body,
)
from database.common import client


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


def create_simulation(name: str) -> Simulation:

    return Simulation(
        **client.table("simulation").insert({"name": name}).execute().data[0]
    )


def fetch_simulation(id: int) -> Simulation:

    return Simulation(
        **client.table("simulation").select("*").eq("id", id).execute().data[0]
    )


def fetch_simulations() -> List[Simulation]:

    return [
        Simulation(**simulation)
        for simulation in client.table("simulation").select("*").execute().data
    ]


def update_simulation(id: int, name: Optional[str] = None) -> Simulation:

    data = {}

    if name is not None:
        data["name"] = name

    if data:
        data["updated_at"] = "now()"

    return Simulation(
        **client.table("simulation").update(data).eq("id", id).execute().data[0]
    )


def delete_simulation(id: int):

    client.table("simulation").delete().eq("id", id).execute()
