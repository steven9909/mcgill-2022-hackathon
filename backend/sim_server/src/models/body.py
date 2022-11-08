from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class Body:
    id: int
    mass: Optional[float]
    position: Optional[np.ndarray]
    velocity: Optional[np.ndarray]
