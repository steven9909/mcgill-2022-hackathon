import numpy as np

class Body:
    def __init__(self, id, mass, p_x, p_y, v_x, v_y):
        self.id = id # unique identifier of the body
        self.mass = mass # mass of this body in kg
        self.pos = np.array([p_x, p_y], dtype=np.float32)
        self.vel = np.array([v_x, v_y], dtype=np.float32)
