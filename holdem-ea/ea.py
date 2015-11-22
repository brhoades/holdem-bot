from generation import Generation

class EA(object):
    def __init__(self, lamb, mu, turns, perturb, sourcefile):
        self.mu   = mu
        self.lamb = lamb

        self.runs = turns 

        # create an initial generation
        self.this_generation = Generation(lamb, mu)
        self.this_generation.random(sourcefile, perturb)

    def run(self):
        for i in range(0,self.runs):
            # this modifies the generation and adds babies
            self.this_generation.reproduce()
            self.this_generation.natural_selection()
