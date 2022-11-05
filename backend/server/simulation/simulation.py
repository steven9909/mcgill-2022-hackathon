from server.simulation.body import Body
from server.simulation.database.redis import RedisDb
from typing import List, Optional
import numpy as np
import threading


class Simulator:
    G = 6.67e-11 # Gravitational constant 
    SIM_T_D = 24.0*60*60 # Default simulation time step
    
    bodies = []
    g_constants = dict()

    is_stopped = False
    is_started = False

    def __init__(self):
        self.redis = RedisDb()

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

                r = (diff[0]**2 + diff[1]**2) ** 1.5
            
                force = -(self.g_constants[(other.id, body.id)] / r) * diff
                resultant_force += force
        
        final_vel = body.vel + resultant_force * d_t / body.mass
        final_pos = body.pos + final_vel * d_t
        
        return (body.id, final_pos, final_vel)

    def _simulate(self, bodies: List[Body], d_t: int, multi_thread: bool = False):
        """
        Simulates one timestep for all bodies

        Args:
            bodies (List[Body]): list of bodies to process the next position and velocity
            d_t (int): time delta in seconds
        """
        next_sim = []

        for body in bodies:
            next_sim.append(self._calculate_next_pos(body, bodies, d_t))

        return next_sim

    def start(self, bodies: List[Body], d_t = SIM_T_D):
        if self.is_stopped or self.is_started:
            return

        self.is_started = True

        self.bodies = bodies

        self.unpause_event = threading.Event()
        self.unpause_event.set()
        
        self.kill_event = threading.Event()

        self.thread = threading.Thread(name = 'event_thread', target=self._run, args=(d_t, ))

        for i in range(0, len(bodies)):
            for j in range(i+1, len(bodies)):
                constant = Simulator.G * bodies[i].mass * bodies[j].mass
                self.g_constants[(bodies[i].id, bodies[j].id)] = constant
                self.g_constants[(bodies[j].id, bodies[i].id)] = constant
        
        self.thread.start()

    def _run(self, d_t = SIM_T_D):
        while True:
            self.unpause_event.wait()

            if self.kill_event.is_set():
                break
            
            if len(self.bodies) <= 1:
                self.unpause_event.clear()

            self.redis.publish_next(self._simulate(self.bodies, d_t))
            
    def pause(self):
        if self.is_stopped or not self.is_started:
            return

        self.unpause_event.clear()

    def resume(self):
        if self.is_stopped or not self.is_started:
            return
        
        self.unpause_event.set()

    def add_body(self, body: Body):
        if self.is_stopped or not self.is_started:
            return

        self.pause()

        for other in self.bodies:
            constant = Simulator.G * other.mass * body.mass
            self.g_constants[(body.id, other.id)] = constant
            self.g_constants[(other.id, body.id)] = constant

        self.bodies.append(body)

        self.resume()

    def update_body(self, id: int, p_x: Optional[float], p_y: Optional[float], v_x: Optional[float], v_y: Optional[float]):
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
        self.is_stopped = True

'''
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

'''