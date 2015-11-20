import json
from sol import Sol

class EA(object):
    def __init__(self, lamb, mu, perturb, sourcefile):
        self.mu   = mu
        self.lamb = lamb

        self.pop  = []
        self.starting_data = json.load(sourcefile)

        # create random solutions with these parameters
        for i in range(0,lamb):
            self.pop.append(Sol(self.starting_data, perturb))
