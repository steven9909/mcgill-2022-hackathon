import numpy as np


class PopBody:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.pos = np.array([start_x, start_y], dtype=np.float32)
        self.vel = np.array([end_x, end_y], dtype=np.float32)
