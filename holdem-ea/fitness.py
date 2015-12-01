from subprocess import Popen
import re
import subprocess
import time
import multiprocessing as mp
#def get_winner(solution1, solution2, rounds):
def get_winner(args):
    """
    Compete in rounds rounds, the one who wins the most is returned.
    Args are packed for 2.7 compatibility with map_async (3.3+ has starmap)
    """
    solution1 = args[0]
    solution2 = args[1]
    rounds = args[2]
    winners = []
    for i in range(rounds):
        winners.append(play_poker(solution1, solution2))

    return winners


def play_poker(solution1, solution2):
    """
    Call our tournament and get the results (return winner).
    """
    p = "java -cp ../../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \"{0}\" \"{1}\"".format(solution1.get_command(),solution2.get_command())

    start = time.time()
    try:
        output = Popen([p], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
    except KeyboardInterrupt:
        return
    t = time.time() - start
    solution1.times.append(t)
    solution2.times.append(t)

    # the last to the third line yields the winner (player1/player2)
    if output[-4][-1] == "1":
        return 1
    else:
        return 2

class FitnessEvaluator(object):
    """
    Pass it a pool size, a 2-d argument list for fitnessfunc, and a fitness func.
    It'll call the function with the pool over and over, with the fitness function
    results being appended into results.
    """
    def __init__(self, size):
        self.size = size
    
    def run(self, args, fitnessfunc):
        if len(args) >= self.size:
            self.pool = mp.Pool(processes=self.size)
            results = []

            try:
                r = self.pool.map_async(fitnessfunc, args, callback=results.extend)
                r = r.get()
                self.pool.close()
                self.pool.join()
            except KeyboardInterrupt:
                self.pool.terminate()
                self.pool.join()
                raise e

            return results
        else:
            # If we've got less work than threads, run on thread
            return [fitnessfunc(arg) for arg in args]
