from solution import Solution
import json
from fitness import play_poker

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
    
    def reproduce(self):
        """
        Create mu children, add them into our generation. Those who reproduce are 
        determined by a tournament. The best always get a chance.
        """
        children = []
        for i in range(0, self.size, 2):
            play_poker(self.pop[i], self.pop[i+1])


    def natural_selection(self):
        pass
