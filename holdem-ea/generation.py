from solution import Solution
import pprint
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
    def __init__(self, size, mu, log):
        self.population = []
        self.size = size
        self.lamb = size
        self.mu   = mu
        self.fiteval = FitnessEvaluator(5)
        self.number = 1
        self.log = log

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
        self.log.debug(pprint.pformat(ranked))
        children = []
        for l in ranked:
            if len(l) == 0:
                ranked.remove(l)
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
        participants = copy(self.population)
        losers = []
        winners = []

        while len(participants) > 1:
            self.log.debug("\nPARTS " + str(len(participants)) + ": ")
            random.shuffle(participants)
            self.log.debug(pprint.pformat(participants))
            args = []
            winners = []

            # pair individuals
            for i in range(0, len(participants), 2):
                if i + 1 >= len(participants):
                    break
                args.append((participants[i], participants[i+1], rounds,))

            # get results, add to losers
            results = self.fiteval.run(args, get_winner)
            for x,a in zip(results, args):
                winners.append(self.handle_winners(x,a))

            # if we have an odd individual, they compete against a random winner
            if len(participants) % 2 != 0:
                opponent = random.sample(winners, 1)[0]
                #winner = self.fiteval.run([(opponent,participants[-1],rounds,)],get_winner)
                # do this on thread. It's just one, and the overhead of creating processes
                # is longer than the function
                args = (opponent, participants[-1], rounds,)
                winner = get_winner(*args)
                winner = self.handle_winners(winner, args)
                if winner is not opponent: # they get to be included... no risk to winner
                    winners.append(participants[-1])
            
            losers.append([x for x in participants if x not in winners])

            self.log.debug("losers:")
            self.log.debug(pprint.pformat(losers))
            participants = winners

        losers.append(winners)
        losers.reverse()
        return losers

    def handle_winners(self, results, participants):
        """
        Have to handle these on thread.
        We're passed a packed results list... 1 for participants[0] winning, 2 for participants[1]
        and we tally up how that affects each.
        """
        for i in results:
            if i == 1:
                participants[0].handle_win(participants[1])
                participants[0].wins += 1
                participants[1].losses += 1
            else:
                participants[1].handle_win(participants[0])
                participants[1].wins += 1
                participants[0].losses += 1
        if results.count(1) > results.count(2):
            return participants[0]
        else:
            return participants[1]


    def natural_selection(self):
        """
        Determine who to kill off. Currently done by tournament selection.
        """
        newpop = []
        self.log.debug("NATURAL SELECTION")

        # another tournament
        results = self.tournament(self.tournament_rounds)
        self.log.debug("RESULTS: ")
        self.log.debug(pprint.pformat(results))

        # first 2 winners will not be eliminated
        for x in results[:2]:
            newpop.extend(x)
            for s in x:
                self.log.debug(s.get_config_file())
                if s in self.population: #this shouldn't be necessary
                    self.population.remove(s)

        self.log.debug("POP: ")
        self.log.debug(pprint.pformat(self.population))
        self.population = sorted(self.population, key=lambda p: p.fitness, reverse=True)
        # top 3 ELO, if not winners, will not be eliminated
        for i in range(3):
            newpop.append(self.population.pop()) 

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
        self.log.debug("\nDetermining Top 7\n")
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
