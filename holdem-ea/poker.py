import random
from solution import Solution
from awesome_print import ap

def copulate(gen, parent1, parent2):
    """
    Randomly averages values or chooses one of parents (50/50).
    Returns a new solution.
    """
    child = Solution(parent1.data, gen) 
    if parent1 is not parent2:
        copulate_recursive(child.data, parent2.data)

    child.update_hash()
    return child


def copulate_recursive(childd, parent2d):
    """
    Recursively combines/shares data dict values
    """
    for k in childd:
        if isinstance(childd[k], int) or isinstance(childd[k], float):
            if random.randint(0,1):
                childd[k] = (childd[k] + parent2d[k]) / 2
            else:
                if random.randint(0,1): # if 1, we change to parent 2... keep otherwise
                    childd[k] = parent2d[k]
        if isinstance(childd[k], dict):
            copulate_recursive(childd[k], parent2d[k])
