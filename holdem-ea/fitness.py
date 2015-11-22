from subprocess import Popen
import re
import subprocess
import time
import multiprocessing as mp
def get_winner(solution1, solution2, rounds):
    """
    Compete in rounds rounds, the one who wins the most is returned.
    """
    winners = []
    for i in range(rounds):
        winners.append(play_poker(solution1, solution2))

    if winners.count(solution1) > rounds/2:
        return solution1
    return solution2


def play_poker(solution1, solution2):
    """
    Call our tournament and get the results (return winner).
    """
    p = "java -cp ../../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \"{0}\" \"{1}\"".format(solution1.get_command(),solution2.get_command())

    start = time.time()
    output = Popen([p], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
    t = time.time() - start
    solution1.times.append(t)
    solution2.times.append(t)
    print(t)

    # the last to the third line yields the winner (player1/player2)
    if output[-4][-1] == "1":
        solution1.wins += 1
        solution2.losses += 1
        return solution1
    else:
        solution2.wins += 1
        solution1.losses += 1
        return solution2

class FitnessEvaluator(object):
    """
    Pass it a pool size, a 2-d argument list for fitnessfunc, and a fitness func.
    It'll call the function with the pool over and over, with the fitness function
    results being appended into results.
    """
    def __init__(self, size):
        self.size = size
    
    def run(self, args, fitnessfunc):
        self.pool = mp.Pool(processes=self.size)

        results = []
        for i in range(len(args)):
            results.append(self.pool.apply_async(fitnessfunc, args[i]))
        self.pool.close()
        self.pool.join()
        # spawn another one so we're ready
        return [x.get() for x in results]