from typing import List, Optional

from database.common import client
from models.simulation import Simulation


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
