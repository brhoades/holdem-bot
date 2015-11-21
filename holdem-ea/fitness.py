from subprocess import Popen
import re
import subprocess
import time
def get_winner(solution1, solution2, rounds):
    """
    Compete in rounds rounds, the one who wins the most is returned.
    """


def play_poker(solution1, solution2):
    """
    Call our tournament and get the results (return winner).
    """
    p = "java -cp ../../texasholdem-engine/bin com.theaigames.game.texasHoldem.TexasHoldem \"{0}\" \"{1}\"".format(solution1.get_command(),solution2.get_command())

    start = time.time()
    output = Popen([p], shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')
    print(time.time() - start)

    # the last to the third line yields the winner (player1/player2)
    if output[-4][-1] == "1":
        return solution1
    else:
        return solution2
