from typing import List
from sim_server.src.simulation.ga.chromosome import Chromosome

class Population:

    def __init__(self, initial_population: List[Chromosome]):
        self.population = initial_population

    def reproduce(self):
        pass