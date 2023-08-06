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
    """ Creates discrete recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # range of parent indexes to sample from 
        idxes = range(parents.pop_size)

        for i in range(offspring.pop_size):
            # pick two parents at random
            p1, p2 = random.sample(idxes, k=2)
            # create offspring
            offspring.individuals[i] = np.array([np.random.permutation(x) 
                                        for x in np.vstack((parents.individuals[p1],parents.individuals[p2])).T]).T[0]
            offspring.sigmas[i] =  np.array([np.random.permutation(x) 
                                        for x in np.vstack((parents.sigmas[p1],parents.sigmas[p2])).T]).T[0]
            if parents.mutation.__class__.__name__ == "Correlated":
                offspring.alphas[i] =  np.array([np.random.permutation(x) 
                                        for x in np.vstack((parents.alphas[p1],parents.alphas[p2])).T]).T[0]


class GlobalDiscrete(Recombination):
    """ Creates discrete recombined offsprings.
    """
    def __call__(self, parents: Population, offspring: Population):
        # range of parent indexes to sample from 
        idxes = range(parents.pop_size)
        
        for i in range(offspring.pop_size):
            # pick two parents at random
            p1, p2 = random.sample(idxes, k=2)
            # create offspring
            offspring.individuals[i] = np.array([np.random.permutation(x) 
                                        for x in parents.individuals.T]).T[0]
            offspring.sigmas[i] =  np.array([np.random.permutation(x) 
                                        for x in parents.sigmas.T]).T[0]
            if parents.mutation.__class__.__name__ == "Correlated":
                offspring.alphas[i] =  np.array([np.random.permutation(x) 
                                        for x in parents.alphas.T]).T[0]
