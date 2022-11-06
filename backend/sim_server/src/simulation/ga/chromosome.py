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
        return (end_y - y) + (end_x - x)