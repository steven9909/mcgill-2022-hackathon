import random
from typing import List

import numpy as np
from simulation.ga.chromosome import Chromosome


class Population:
    def __init__(
        self, initial_population: List[Chromosome], start_x, start_y, end_x, end_y
    ):
        self.chromosomes = initial_population
        self.n = len(initial_population)
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def reproduce(self, elite_percentage=0.05, mutation_rate=0.02):
        self.chromosomes.sort(key=lambda x: x.fitness)

        elites = self.chromosomes[0 : int(self.n * elite_percentage)]

        for _ in range(self.n - len(elites)):
            elites.append(self._crossover(*self._select_parents()))

        for individual in elites:
            m = random.random()
            if m < mutation_rate:
                individual.mutate()

        self.chromosomes = elites

    def _select_parents(self):
        fitnesses = np.array(
            [1 / chromosome.fitness for chromosome in self.chromosomes]
        )
        fitnesses /= fitnesses.sum()
        return np.random.choice(self.chromosomes, 2, replace=False, p=fitnesses)

    def _crossover(self, parent1: Chromosome, parent2: Chromosome):
        return Chromosome(
            (parent1.force + parent2.force) / 2,
            (parent1.angle + parent2.angle) / 2,
            self.start_x,
            self.end_x,
            self.start_y,
            self.end_y,
        )
