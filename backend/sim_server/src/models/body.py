from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class Body:
    id: int
    mass: Optional[float]
    position: Optional[np.ndarray]
    velocity: Optional[np.ndarray]

    def to_json(self):
        return {
            "id": self.id,
            "mass": self.mass,
            "position": {"x": self.position[0], "y": self.position[1]},
            "velocity": {"x": self.velocity[0], "y": self.velocity[1]},
        }
