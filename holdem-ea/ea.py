from generation import Generation
import os
import logging
import logging.handlers

class EA(object):
    def __init__(self, lamb, mu, turns, perturb, sourcefile):
        self.mu   = mu
        self.lamb = lamb

        self.runs = turns 

        LOG_FILENAME = os.path.abspath("./results/ealog.txt")

        # Set up a specific logger with our desired output level
        self.log = logging.getLogger('MyLogger')
        self.log.setLevel(logging.DEBUG)

        self.handler = logging.handlers.RotatingFileHandler(
                LOG_FILENAME, backupCount=5)

        self.log.addHandler(self.handler)

        # create an initial generation
        self.this_generation = Generation(lamb, mu, self.log)
        self.this_generation.random(sourcefile, perturb)

    def run(self):
        for i in range(0,self.runs):
            print("\n\n=====\nGENERATION: {0}\n====".format(self.this_generation.number))
            self.log.debug("\n\n=====\nGENERATION: {0}\n====".format(self.this_generation.number))
            # this modifies the generation and adds babies
            self.this_generation.reproduce()
            self.this_generation.natural_selection()

            if self.this_generation.number % 10 == 0:
                self.this_generation.every_ten_tournament()

            self.this_generation.output_statistics()
            self.this_generation.number += 1

            self.output_top()

    def output_top(self):
        num = 10
        sols = []

        for s in sorted(self.this_generation.population, key=lambda p: p.fitness, reverse=True):
            sols.append(s)
        self.this_generation.output_solutions_to_file(sols,"top10.txt")
