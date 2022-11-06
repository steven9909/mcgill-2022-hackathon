from sim_server.src.simulation.body import Body
from sim_server.src.simulation.database.redis import RedisDb
from sim_server.src.simulation.ga.population import Population
from sim_server.src.simulation.ga.chromosome import Chromosome
from typing import List, Optional
import random
import numpy as np
import threading
import math
import time


class Simulator:
    G = 6.67e-11  # Gravitational constant
    SIM_T_D = 240  # Default simulation time step

    bodies = []
    g_constants = dict()

    is_stopped = False
    is_started = False

    def __init__(self):
        self.redis = RedisDb()
        self.population = None
        self.start_time = None
        self.population_bodies = None

    def _calculate_next_pos(self, body: Body, others: List[Body], d_t: int):
        """
        Calculates next position and velocity of body taking into account others.
        This performs all calculations, regardless of whether the effect of other bodies is neglible or not.

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

                force = -(self.g_constants[(other.id, body.id)] / r) * diff
                resultant_force += force

        final_vel = body.vel + resultant_force * d_t / body.mass
        final_pos = body.pos + final_vel * d_t
        
        return (body.id, final_pos, final_vel)

    def _simulate_agents(self, bodies: List[Body]):
        if self.population_bodies is None:
            return

        next_sim = []
        for i, agent_body in enumerate(self.population_bodies):
            next_pos = self._calculate_next_pos(agent_body, bodies, self.d_t)
            x = next_pos[1][0]
            y = next_pos[1][1]
            self.population.chromosomes[i].update_fitness(x, self.end_x, y, self.end_y)
            agent_body.pos = next_pos[1]
            agent_body.vel = next_pos[2]
            next_sim.append(next_pos)
        
        return next_sim

    def _simulate_bodies(self, bodies: List[Body]):
        """
        Simulates one timestep for all bodies

        Args:
            bodies (List[Body]): list of bodies to process the next position and velocity
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

        self.thread = threading.Thread(
            name="event_thread", target=self._run
        )

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

            if self.start_time is not None and (time.time_ns() - self.start_time)//1000000000 > self.timeout:
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

    def _reset_population(self):
        self.pause()
        self.population.reproduce()

        self.population_bodies.clear()
        for i, chromosome in enumerate(self.population.chromosomes):
            v_x = (chromosome.force * math.cos(chromosome.angle) / self.agent_mass) * self.d_t
            v_y = (chromosome.force * math.sin(chromosome.angle) / self.agent_mass) * self.d_t

            self.population_bodies.append(Body(-1-i, self.agent_mass, self.start_x, self.start_y, v_x, v_y))

        self.start_time = time.time_ns()
        self.resume()

    def initialize_population(self, start_x, start_y, end_x, end_y, timeout = 120, num_populations = 100, agent_mass = 50):
        if self.is_stopped or not self.is_started:
            return
        self.pause()

        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.timeout = timeout
        self.agent_mass = agent_mass

        chromosomes = [Chromosome(random.random() * Chromosome.FORCE_LIMIT, random.random() * 2 * math.pi, start_x, end_x, start_y, end_y) for _ in range(num_populations)]

        self.population = Population(chromosomes, start_x, start_y, end_x, end_y)

        self.population_bodies = []
        for i, chromosome in enumerate(chromosomes):
            v_x = (chromosome.force * math.cos(chromosome.angle) / agent_mass) * self.d_t
            v_y = (chromosome.force * math.sin(chromosome.angle) / agent_mass) * self.d_t

            self.population_bodies.append(Body(-1-i, agent_mass, start_x, start_y, v_x, v_y))

        for body in self.bodies:
            constant = Simulator.G * agent_mass * body.mass
            self.g_constants[(-1, body.id)] = constant
            self.g_constants[(body.id, -1)] = constant

        self.start_time = time.time_ns()

        self.resume()

    def add_body(self, body: Body):
        if self.is_stopped:
            return

        if self.is_started:
            self.pause()

        for other in self.bodies:
            constant = Simulator.G * other.mass * body.mass
            self.g_constants[(body.id, other.id)] = constant
            self.g_constants[(other.id, body.id)] = constant

        if self.population_bodies is not None and len(self.population_bodies) >= 1:
            constant = Simulator.G * self.agent_mass * body.mass
            self.g_constants[(body.id, -1)] = constant
            self.g_constants[(-1, body.id)] = constant

        self.bodies.append(body)

        if self.is_started:
            self.resume()

    def update_body(
        self,
        id: int,
        p_x: Optional[float],
        p_y: Optional[float],
        v_x: Optional[float],
        v_y: Optional[float],
    ):
        if self.is_stopped or not self.is_started:
            return

        self.pause()

        for body in self.bodies:
            if body.id == id:
                body.pos[0] = p_x if p_x is not None else body.pos[0]
                body.pos[1] = p_y if p_y is not None else body.pos[1]
                body.vel[0] = v_x if v_x is not None else body.vel[0]
                body.vel[1] = v_y if v_y is not None else body.vel[1]
                break

        self.resume()

    def remove_body(self, id: int):
        if self.is_stopped or not self.is_started:
            return

        self.pause()

        self.bodies = [body for body in self.bodies if not body.id == id]

        self.resume()

    def stop(self):
        if not self.is_started:
            return
            
        self.kill_event.set()
        self.resume()
        self.population = None
        self.start_time = None
        self.population_bodies = None
        self.is_stopped = True
        self.is_started = False
        self.g_constants.clear()
        self.bodies.clear()

Ms = 2.0e30         
Mm = 6.39e23
Me = 5.972e24   

xe, ye = 1.0167*1.5e11, 0
xve, yve = 0, 29290

xm, ym = 1.5*1.5e11, 0
xvm, yvm = 0, 24070

xs,ys = 0,0
xvs,yvs = 0,0

sim = Simulator()
sim.start([Body(1, Me, xe, ye, xve, yve), Body(2, Ms, xs, ys, xvs, yvs), Body(3, Mm, xm, ym, xvm, yvm)])

"""
G = 6.67e-11                 
Ms = 2.0e30         
Mm = 6.39e23
Me = 5.972e24         
days_in_sec = 24.0*60*60         

xe, ye = 1.0167*1.5e11, 0
xve, yve = 0, 29290

xm, ym = 1.5*1.5e11, 0
xvm, yvm = 0, 24070

xs,ys = 0,0
xvs,yvs = 0,0
t = 0.0
d_t = days_in_sec

xelist,yelist = [],[]
xmlist, ymlist = [], []
xslist,yslist = [],[]

sim = Simulator()

while t < 687*days_in_sec:

    next_sim = sim.start([Body(1, Me, xe, ye, xve, yve), Body(2, Ms, xs, ys, xvs, yvs), Body(3, Mm, xm, ym, xvm, yvm)], d_t)
 
    xe = next_sim[0][1][0]
    ye = next_sim[0][1][1]
    xve = next_sim[0][2][0]
    yve = next_sim[0][2][1]

    xs = next_sim[1][1][0]
    ys = next_sim[1][1][1]
    xvs = next_sim[1][2][0]
    yvs = next_sim[1][2][1]

    xm = next_sim[2][1][0]
    ym = next_sim[2][1][1]
    xvm = next_sim[2][2][0]
    yvm = next_sim[2][2][1]

    xelist.append(xe)
    yelist.append(ye)

    xmlist.append(xm)
    ymlist.append(ym)

    xslist.append(xvs)
    yslist.append(yvs)
  
    t += d_t

plt.plot(xelist,yelist,'r',lw=2)
plt.plot(xmlist,ymlist,'g',lw=2)
plt.axis('equal')
plt.show()

"""
