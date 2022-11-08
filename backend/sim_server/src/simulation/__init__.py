import threading
from typing import Dict

import numpy as np
import redis
from models.body import Body
import json


class Simulator:
    G = 6.674e-11
    dt = 60 * 60 * 24

    def __init__(self):

        self.db = redis.StrictRedis(
            "localhost", 6379, charset="utf-8", decode_responses=True
        )
        self.bodies: Dict[int, Body] = {}
        self.bodies_access_lock = threading.Lock()
        self.start_event = threading.Event()
        self.stop_event = threading.Event()

    def _calc_force(self, r1: np.ndarray, r2: np.ndarray, mass1: float, mass2: float):

        r21 = r2 - r1

        return self.G * (mass1 * mass2 / np.linalg.norm(r21) ** 3) * r21

    def _update_body(self, body: Body):

        resultant_force = np.zeros(2)

        for other_body in self.bodies.values():
            if body.id == other_body.id:
                continue

            resultant_force += self._calc_force(
                body.position, other_body.position, body.mass, other_body.mass
            )

        acceleration = resultant_force / body.mass  # a = f / m
        body.velocity = body.velocity + acceleration * self.dt
        body.position = body.position + body.velocity * self.dt

    def _update_bodies(self):

        for body in self.bodies.values():
            self._update_body(body)

    def _task(self):

        self.start_event.set()

        while True:
            if self.stop_event.is_set():
                break

            self._update_bodies()
            self.db.publish(
                "bodies", json.dumps([body.to_json() for body in self.bodies.values()])
            )

        self.start_event.clear()

    def start(self):
        self.stop_event.clear()

        if not self.start_event.is_set():
            threading.Thread(target=self._task).start()

    def stop(self):

        self.stop_event.set()

    def create_body(self, body: Body):

        with self.bodies_access_lock:
            if body.id in self.bodies:
                return

            self.bodies[body.id] = body

    def update_body(self, body: Body):

        with self.bodies_access_lock:
            if body.id not in self.bodies:
                return

            if body.mass is not None:
                self.bodies[body.id].mass = body.mass

            if body.position is None:
                self.bodies[body.id].position = body.position

            if body.velocity is None:
                self.bodies[body.id].velocity = body.velocity

    def delete_body(self, id: int):

        with self.bodies_access_lock:
            del self.bodies[id]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    sim = Simulator()
    sim.create_body(Body(1, 1.989e30, np.array([0, 0]), np.array([0, 0])))
    sim.create_body(
        Body(2, 5.972e24, np.array([149.600e9, 0]), np.array([0, 30.000e3]))
    )

    s = []
    e = []

    for i in range(365 // 4):
        s.append((sim.bodies[1].position[0], sim.bodies[1].position[1]))
        e.append((sim.bodies[2].position[0], sim.bodies[2].position[1]))
        sim._update_bodies()

    plt.scatter(*zip(*s))
    plt.scatter(*zip(*e))
    plt.show()
