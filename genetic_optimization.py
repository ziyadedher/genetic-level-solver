class Population:

    def __init__(self):
        self.individuals = Individual[50] # create Individual class

        for i in range(len(self.individuals)):
             self.individuals[i] = Individual();


class Individual:

    def __init__(self):
        # initialize with random values for numNodes, numMuscles, strengths, , lengths etc.
        # possibl


    def find_fitness(self):
        # create fitness function
