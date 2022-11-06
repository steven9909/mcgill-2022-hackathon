from math import sqrt, abs

class Chromosome:
    
    FORCE_LIMIT = 10000

    def __init__(self, force: float, angle: float):
        """ 
        Constructor for chromosome

        Args:
            force (float): force in newtons 
            angle (float): angle in radians relative to positive x axis
        """

        self.force = force if force < Chromosome.FORCE_LIMIT else Chromosome.FORCE_LIMIT
        self.angle = angle

    def fitness(self, x: float, y: float, end_x: float, end_y: float):
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
        return sqrt(abs(end_y - y)**2 + abs(end_x - x)**2)