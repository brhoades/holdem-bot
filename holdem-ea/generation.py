from solution import Solution
import json

class Generation(object):
    """
    A generation houses a collection of solutions.
    """
    def __init__(self, size):
        self.pop = []
        self.size = size

    def random(self, sourcefile, perturb):
        starting_data = json.load(sourcefile)

        # create random solutions with these parameters
        for i in range(0,self.size):
            self.pop.append(Solution(starting_data, perturb))

    def load_population(self, population):
        self.pop = population
