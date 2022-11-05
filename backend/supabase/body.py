from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from common import client


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


def create_body(
    simulation_id: int,
    mass: float,
    initial_position: Vec2,
    initial_velocity: Vec2,
    model_path: str,
) -> Body:

    return Body(
        **(
            client.table("body")
            .insert(
                {
                    "simulation_id": simulation_id,
                    "mass": mass,
                    "initial_position": initial_position.dict(),
                    "initial_velocity": initial_velocity.dict(),
                    "model_path": model_path,
                }
            )
            .execute()
        ).data[0]
    )


def fetch_body(id: int, simulation_id: int) -> Body:

    return Body(
        **client.table("body")
        .select("*")
        .eq("id", id)
        .eq("simulation_id", simulation_id)
        .execute()
        .data[0]
    )


def fetch_bodies(simulation_id: int) -> List[Body]:

    return [
        Body(**body)
        for body in client.table("body")
        .select("*")
        .eq("simulation_id", simulation_id)
        .execute()
        .data
    ]


def update_body(
    id: int,
    simulation_id: int,
    mass: Optional[float] = None,
    initial_position: Optional[Vec2] = None,
    initial_velocity: Optional[Vec2] = None,
    model_path: Optional[str] = None,
) -> Body:

    data = {}

    if mass is not None:
        data["mass"] = mass

    if initial_position is not None:
        data["initial_position"] = initial_position.dict()

    if initial_velocity is not None:
        data["initial_velocity"] = initial_velocity.dict()

    if model_path is not None:
        data["model_path"] = model_path.dict()

    if data:
        data["updated_at"] = "now()"

    return Body(
        **client.table("body")
        .update(data)
        .eq("id", id)
        .eq("simulation_id", simulation_id)
        .execute()
        .data[0]
    )


def delete_body(id: int, simulation_id: int):

    client.table("body").delete().eq("id", id).eq(
        "simulation_id", simulation_id
    ).execute()
