class Population(object):
    """A collection of Individual objects"""
    def __init__(self, amount):
        individuals = [] # create empty Individuals list

        for individual_index in range(amount):
            individuals[individual_index] = Individual()

class Individual(object):
    """An individual creature"""
    def __init__(self):
        pass
