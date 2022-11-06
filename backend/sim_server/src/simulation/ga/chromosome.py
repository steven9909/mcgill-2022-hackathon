class Chromosome:
    
    FORCE_LIMIT = 10000

    def __init__(self, force: float, angle: float):
        """ 
        Constructor for chromosome

        Args:
            force (float): force in newtons 
            angle (float): angle in degrees relative to body
        """

        self.force = force if force < Chromosome.FORCE_LIMIT else Chromosome.FORCE_LIMIT
        self.angle = angle