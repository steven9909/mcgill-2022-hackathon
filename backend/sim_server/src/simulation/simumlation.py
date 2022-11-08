import math
import random
import threading
import time
from typing import Dict, List, Optional

import numpy as np
import redis
from models.body import Body
from simulation.ga.chromosome import Chromosome
from simulation.ga.population import Population


class Simulator:
    G = 6.674e-11  # Gravitational constant
    SIM_T_D = 360  # Default simulation time step

    bodies = []
    g_constants = dict()

    is_stopped = False
    is_started = False

    def __init__(self):
        self.redis = redis.StrictRedis(
            "localhost", 6379, charset="utf-8", decode_responses=True
        )
        self.bodies: Dict[int, Body] = {}
        self.bodies_access_lock = threading.Lock()

        self.population = None
        self.start_time = None
        self.population_bodies = []
        self.player_body = None
        self.d_t = Simulator.SIM_T_D

    def _calculate_next_pos(self, body: Body, others: List[Body], d_t: int):
        """
        Calculates next position and velocity of body taking into account others.
        This performs all calculations, regardless of whether the effect of other
        bodies is neglible or not.

        Args:
            body (Body): The body to predict the next pos/vel
            others (List[Body]): Other bodies
            d_t (int): Time step

        Returns:
            _type_: _description_
        """

        resultant_force = np.zeros((2), dtype=np.float32)

        for other in others:
            if not other.id == body.id:
                diff = body.pos - other.pos

                r = (diff[0] ** 2 + diff[1] ** 2) ** 1.5
                id = body.id
                if body.id <= -1:
                    id = -1
                force = -(self.g_constants[(other.id, id)] / r) * diff
                resultant_force += force

        final_vel = body.vel + resultant_force * d_t / body.mass
        final_pos = body.pos + final_vel * d_t

        return (body.id, final_pos, final_vel)

    def _simulate_bodies(self, bodies: List[Body]):
        """
        Simulates one timestep for all bodies

        Args:
            bodies (List[Body]): list of bodies to process the next position and
            velocity
        """
        next_sim = []

        for body in bodies:
            next_body = self._calculate_next_pos(body, bodies, self.d_t)
            next_sim.append(next_body)

            body.pos = next_body[1]
            body.vel = next_body[2]

        return next_sim

    def start(self, bodies: List[Body], d_t=SIM_T_D):
        if self.is_started:
            return

        self.is_stopped = False
        self.is_started = True

        self.d_t = d_t

        self.bodies = bodies

        self.unpause_event = threading.Event()
        self.unpause_event.set()

        self.kill_event = threading.Event()

        self.thread = threading.Thread(name="event_thread", target=self._run)

        for i in range(0, len(bodies)):
            for j in range(i + 1, len(bodies)):
                constant = Simulator.G * bodies[i].mass * bodies[j].mass
                self.g_constants[(bodies[i].id, bodies[j].id)] = constant
                self.g_constants[(bodies[j].id, bodies[i].id)] = constant

        self.thread.start()

    def _run(self):
        while True:
            self.unpause_event.wait()

            if self.kill_event.is_set():
                break

            if len(self.bodies) <= 1 and self.population is None:
                self.unpause_event.clear()

            if (
                self.start_time is not None
                and (time.time_ns() - self.start_time) // 1000000000 > self.timeout
            ):
                self._reset_population()
                continue

            self.redis.publish_next_bodies(self._simulate_bodies(self.bodies))
            self.redis.publish_next_agents(self._simulate_agents(self.bodies))

    def pause(self):
        if self.is_stopped or not self.is_started:
            return

        self.unpause_event.clear()

    def resume(self):
        if self.is_stopped or not self.is_started:
            return

        self.unpause_event.set()

    def create_body(self, body: Body):

        with self.bodies_access_lock:
            self.bodies[body.id] = body

    def update_body(self, body: Body):

        with self.bodies_access_lock:
            self.bodies[body.id] = body

    def delete_body(self, id: int):

        with self.bodies_access_lock:
            del self.bodies[id]

    def stop(self):
        if not self.is_started:
            return

        self.kill_event.set()
        self.resume()
        self.population = None
        self.start_time = None
        self.population_bodies.clear()
        self.is_stopped = True
        self.is_started = False
        self.g_constants.clear()
        self.bodies.clear()
