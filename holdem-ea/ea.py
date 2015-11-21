from generation import Generation

class EA(object):
    def __init__(self, lamb, mu, turns, perturb, sourcefile):
        self.mu   = mu
        self.lamb = lamb

        self.runs = turns 

        # create an initial generation
        self.this_generation = Generation(mu)
        self.this_generation.random(sourcefile, perturb)

    def run(self):
        for i in range(0,self.runs):
            pass

