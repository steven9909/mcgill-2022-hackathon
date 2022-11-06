from math import sqrt, abs, pi
import random

class Chromosome:
    
    FORCE_LIMIT = 10000

    def __init__(self, force: float, angle: float, start_x: float, end_x:float, start_y: float, end_y: float):
        """ 
        Constructor for chromosome

        Args:
            force (float): force in newtons 
            angle (float): angle in radians relative to positive x axis
        """

        self.force = force if force < Chromosome.FORCE_LIMIT else Chromosome.FORCE_LIMIT
        self.angle = angle
        self.fitness = self.fitness_func(start_x, end_x, start_y, end_y)

    def update_fitness(self, x: float, end_x: float, y: float, end_y: float):
        self.fitness = min(self.fitness, self.fitness_func(x, end_x, y, end_y))

    def fitness_func(self, x: float, end_x: float, y: float, end_y: float):
        """
        Calculate the fitness of a chromosome using Euclidean distance

        Args:
            x (float): _description_
            y (float): _description_
            end_x (float): _description_
            end_y (float): _description_

        Returns:
            _type_: _description_
        """
        return abs(end_y - y)**2 + abs(end_x - x)**2

    def mutate(self, n_m = 20):
        """
        Perform polynomial mutation

        Args:
            n_m (int, optional): user defined parameter that controls how far to deviate from current value when mutated. Defaults to 20.
        """
        u = random.random()

        if u <= 0.5:
            d_l = (2 * u)**(1 / (1 + n_m)) - 1
            self.force = self.force + d_l * self.force
            self.angle = self.angle + d_l * self.angle
        else:
            d_r = 1 - (2 * (1 - u)) * (1 / (1 + n_m))
            self.force = self.force + d_r * (Chromosome.FORCE_LIMIT - self.force)
            self.angle = self.angle + d_r * (2 * pi - self.angle)
