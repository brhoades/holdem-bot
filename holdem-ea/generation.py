from solution import Solution
import random
import json
from fitness import get_winner, FitnessEvaluator
from copy import copy

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

        self.tournamentrounds = 3

    def random(self, sourcefile, perturb):
        starting_data = json.load(sourcefile)

        # create random solutions with these parameters
        for i in range(0,self.size):
            self.population.append(Solution(starting_data, perturb))

    def load_population(self, population):
        self.population = population
    
    def reproduce(self):
        """
        Create mu children, add them into our generation. Those who reproduce are 
        determined by a tournament. The best always get a chance.
        """
        parents = self.tournament()

    def tournament(self):
        """
        Rather than running a turnment size times, I've elected to do a single tournament
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
            for i in range(0, len(participants), 2):
                if i + 1 >= len(participants):
                    break
                args.append((participants[i], participants[i+1], self.tournamentrounds,))

            winners = self.fiteval.run(args, get_winner)
            losers.extend([x for x in participants if x not in winners])

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
        return (losers + participants).reverse()


    def natural_selection(self):
        pass
