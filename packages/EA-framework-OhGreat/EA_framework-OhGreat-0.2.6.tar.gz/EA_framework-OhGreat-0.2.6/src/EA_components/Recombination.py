from EA_components.Population import *
import numpy as np
import random


class Recombination:
    def __call__(self):
        pass


class Intermediate(Recombination):
    """ Creates offspring by taking the average values of the parents
    """
    def __call__(self, parents: Population, offspring: Population):
        # range of parent indexes to sample from 
        idxes = range(parents.pop_size)

        for i in range(offspring.pop_size):
            # pick two parents at random
            p1, p2 = random.sample(idxes, k=2)
            # update offspring population
            offspring.individuals[i] = (parents.individuals[p1] + parents.individuals[p2]) / 2
            offspring.sigmas[i] = (parents.sigmas[p1] + parents.sigmas[p2]) / 2
            # recombine alphas if we are using them
            if parents.mutation.__class__.__name__ == "Correlated":
                offspring.alphas[i] = (parents.alphas[p1] + parents.alphas[p2]) / 2


class GlobalIntermediary(Recombination):
    """ Generates one offspring as the mean value of all the parents.
    """
    def __call__(self, parents: Population, offspring: Population):
        offspring.individuals = parents.individuals.mean(axis=0, keepdims=True)
        offspring.sigmas = parents.sigmas.mean(axis=0)
        if parents.mutation.__class__.__name__ == "Correlated":
                offspring.alphas = parents.alphas.mean(axis=0, keepdims=True)


class Discrete(Recombination):
    """ Creates discretely recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # reset offspring
        offspring.individuals = []
        offspring.sigmas = []
        for _ in range(offspring.pop_size):
            # sample parent individuals
            p1, p2 = random.sample(range(parents.pop_size), k=2)
            # create new individual
            offspring.individuals.append([par_1 if random.uniform(0, 1) > .5 else par_2
                            for par_1, par_2 in zip(parents.individuals[p1],parents.individuals[p2])])
            # create new sigmas for individual
            offspring.sigmas.append([sig_1 if random.uniform(0, 1) > .5 
                    else sig_2 for sig_1, sig_2 in zip(parents.sigmas[p1], parents.sigmas[p2])])
        
        offspring.individuals = np.array(offspring.individuals)
        offspring.sigmas = np.array(offspring.sigmas)


class GlobalDiscrete(Recombination):
    """ Creates discrete recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # reset offspring
        offspring.individuals = []
        offspring.sigmas = []
        for _ in range(offspring.pop_size):
            offspring.individuals.append([random.sample(list(x), k=1)[0] for x in parents.individuals.T])
            offspring.sigmas.append([random.sample(list(x), k=1)[0] for x in parents.sigmas.T])
        offspring.individuals = np.array(offspring.individuals)
        offspring.sigmas = np.array(offspring.sigmas)
