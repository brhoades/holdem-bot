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
            print("\n\n=====\nGENERATION: {0}\n====".format(self.this_generation.number))
            # this modifies the generation and adds babies
            self.this_generation.reproduce()
            self.this_generation.natural_selection()
            self.this_generation.number += 1
            
            avgtime = 0
            avgfitness = 0
            avggen = 0
            best = None
            for s in self.this_generation.population:
                if len(s.times) > 0:
                    avgtime += s.average_time
                avgfitness += s.fitness
                if best is None or s.fitness > best.fitness:
                    best = s
                avggen += s.generation

            avgfitness /= len(self.this_generation.population)
            avgtime /= len(self.this_generation.population)
            avggen /= len(self.this_generation.population)

            print("\nType\tFit\tTime\tGen")
            print("Avg\t{0}\t{1}\t{2}".format(round(avgtime,2),round(avgfitness,2),round(avggen,2)))
            print("Best\t{0}\t{1}\t{2}\t{3}/{4}".format(round(best.fitness,2),
                round(best.average_time,2),round(best.generation,2),best.wins,best.losses))

            self.output_top()

    def output_top(self):
        num = 10
        with open('topten.txt','w') as f:
            f.write("\nType\tFit\tTime\tGen\n")
            for s in sorted(self.this_generation.population, key=lambda p: p.fitness, reverse=True):
                num -= 1
                f.write("{0}\t{1}\t{2}\t{3}\t{4}\n    {5}\n".format(s.generation, s.fitness, s.wins, s.losses, \
                    s.average_time, s.get_config_file()))

                if num < 0:
                    return
