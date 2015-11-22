from solution import Solution
from awesome_print import ap
from fitness import get_winner, FitnessEvaluator
from copy import copy
from numpy.random import choice
from poker import copulate
import os
import random
import json

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

        self.results_folder = "./results"

        self.tournament_rounds = 3
        self.mutation_rate = 0.1

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
        ranked = self.tournament(self.tournament_rounds)
        children = []
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
        
        for child in children:
            if random.random() <= self.mutation_rate:
                child.mutate()

        #plus strategy
        self.population += children

    def tournament(self, rounds):
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
            #print "\nPARTS " + str(len(participants)) + ": ",
            random.shuffle(participants)
            args = []
            # pair individuals
            for i in range(0, len(participants), 2):
                if i + 1 >= len(participants):
                    break
                args.append((participants[i], participants[i+1], rounds,))

            # get results, add to losers
            winners = self.fiteval.run(args, get_winner)
            losers.append([x for x in participants if x not in winners])

            # if we have an odd individual, they compete against a random winner
            if len(participants) % 2 != 0:
                opponent = random.sample(winners, 1)[0]
                winner = self.fiteval.run([(opponent,participants[-1],rounds,)],get_winner)
                if winner is not opponent: # they get to be included... no risk to winner
                    winners.extend(winner)
                else:
                    losers[-1].append(participants[-1])
            
            participants = winners

        losers.append(winners)
        losers.reverse()
        return losers


    def natural_selection(self):
        """
        Determine who to kill off. Currently done by tournament selection.
        """
        newpop = []

        # top 3 ELO, if not winners, will not be eliminated
        count = 0
        self.population = sorted(self.population, key=lambda p: p.fitness)
        for i in range(3):
            newpop.append(self.population.pop()) 
            count += 1

        # another tournament
        results = self.tournament(self.tournament_rounds)

        # first 3 winners will not be eliminated
        for x in results[:2]:
            newpop.extend(x)

        results = results[2:]

        # sort our levels
        for l in results:
            l = sorted(l, key=lambda p: p.fitness, reverse=True)

        # now randomly pop elements off
        while len(newpop) < self.lamb:
            l = random.sample(results,1)[0]
            newpop.append(l.pop())
            if len(l) == 0:
                results.remove(l)
        self.population = newpop
        
    def every_ten_tournament(self):
        """
        Every 10 generations we have a tournament. It's best out of 7
        and the top 7 are output to results/every10/tournament_gen#.txt
        """
        print("\nDetermining Top 7\n")
        ranked = self.tournament(7)
        winners = []
        for x in ranked[:3]:
            winners.extend(x)

        filename = os.path.join("generation_{0}.txt".format(self.number))
        self.output_solutions_to_file(winners, filename)


    def output_solutions_to_file(self, solutions, filename):
        """
        Takes a list of solutions and outputs them to a filename in results/.
        """
        if not os.path.exists(os.path.abspath(self.results_folder)):
            os.mkdir(os.path.abspath(self.results_folder))
        filename = os.path.join(os.path.abspath(self.results_folder),filename)
        with open(filename,'w') as f:
            f.write("Gen\tFit\tWins\tLosses\tTime\n")
            for s in solutions:
                f.write("{0}\t{1}\t{2}\t{3}\t{4}\n    {5}\n".format(s.generation, round(s.fitness), s.wins, s.losses, \
                    round(s.average_time,2), s.get_config_file()))
