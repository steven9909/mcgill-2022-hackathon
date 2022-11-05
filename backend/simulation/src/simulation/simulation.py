from src.simulation.body import Body
from typing import List
import numpy as np
import matplotlib.pyplot as plt

class Simulator:
    G = 6.67e-11 # Gravitational constant 
    SIM_T_D = 24.0*60*60 # Default simulation time step

    @staticmethod
    def _calculate_next_pos(body: Body, others: List[Body], d_t: int):
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
            
                force = -(Simulator.G * body.mass * other.mass / r) * diff
                resultant_force += force
        
        final_vel = body.vel + resultant_force * d_t / body.mass
        final_pos = body.pos + final_vel * d_t
        
        return (body.id, final_pos, final_vel)

    @staticmethod
    def _simulate(bodies: List[Body], d_t: int):
        """
        Simulates one timestep for all bodies

        Args:
            bodies (List[Body]): list of bodies to process the next position and velocity
            d_t (int): time delta in seconds
        """
        next_sim = []

        for body in bodies:
            next_sim.append(Simulator._calculate_next_pos(body, bodies, d_t))

        return next_sim

    @staticmethod
    def start(d_t = SIM_T_D):
        """ starts
        """
        pass

    @staticmethod
    def stop():
        """_summary_
        """

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

while t < 687*days_in_sec:

    next_sim = Simulator._simulate([Body(1, Me, xe, ye, xve, yve), Body(2, Ms, xs, ys, xvs, yvs), Body(3, Mm, xm, ym, xvm, yvm)], d_t)
 
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
    
print(xslist)
plt.plot(xelist,yelist,'r',lw=2)
plt.plot(xmlist,ymlist,'g',lw=2)
plt.axis('equal')
plt.show()
'''