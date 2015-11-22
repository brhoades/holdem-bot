from solution import Solution
import random
import json
from fitness import get_winner, FitnessEvaluator
from copy import copy
from numpy.random import choice
from poker import copulate

class Generation(object):
    """
    A generation houses a collection of solutions.
    """
    def __init__(self, size, mu):
        self.population = []
        self.size = size
        self.lamb = size
        self.mu   = mu
        self.fiteval = FitnessEvaluator(10)
        self.number = 1

        self.tournamentrounds = 3

    def random(self, sourcefile, perturb):
        starting_data = json.load(sourcefile)

        # create random solutions with these parameters
        for i in range(0,self.size):
            self.population.append(Solution(starting_data, self.number, perturb))

    def load_population(self, population):
        self.population = population
    
    def reproduce(self):
        """
        Create mu children, add them into our generation. Those who reproduce are 
        determined by a tournament. The best always get a chance.
        """
        ranked = self.tournament()
        children = []
        # sort our levels
        for l in ranked:
            l = sorted(l, key=lambda p: p.fitness, reverse=True)

        for i in range(self.mu):
            parents = []
            for i in range(2):
                # Randomly select from hierarchy, upper has the most chance for individuals
                # as there are fewer members... all hierarchies have equal chance.
                level = random.sample(ranked,1)[0]
                # individuals  are then chosen randomly, weighted by fitness (W:L)
                #parents.append(choice(level, [x.fitness for x in level]))
                # parents chosen randomly
                parents.append(random.sample(level,1)[0])
            children.append(copulate(self.number, *parents))
        
        self.mutate(children)

    def mutate(self, children):
        pass


    def tournament(self):
        """
        Rather than running a tournament size times, I've elected to do a single tournament
        (3 rounds per by default) that then returns a list of ranked individuals.
        This list returned is 2d. Starting with the best, each list contains 2*last
        entries for where contestants were eliminated.
        """
        args = []
        participants = copy(self.population)
        losers = []
        winners = []

        while len(participants) > 1:
            print("PARTS: " + str(len(participants)))
            random.shuffle(participants)
            args = []
            # pair individuals
            for i in range(0, len(participants), 2):
                if i + 1 >= len(participants):
                    break
                args.append((participants[i], participants[i+1], self.tournamentrounds,))

            # get results, add to losers
            winners = self.fiteval.run(args, get_winner)
            losers.append([x for x in participants if x not in winners])

            # if we have an odd individual, they compete against a random winner
            if len(participants) % 2 != 0:
                print("SPECIAL CONTESTANT")
                opponent = random.sample(winners, 1)[0]
                winner = self.fiteval.run([(opponent,participants[-1],self.tournamentrounds,)],get_winner)
                if winner is not opponent: # they get to be included... no risk to winner
                    winners.extend(winner)
                else:
                    losers[-1].append(participants[-1])
            
            participants = winners

        losers.append(participants)
        losers.reverse()
        return losers


    def natural_selection(self):
        pass
