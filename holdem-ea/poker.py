import random
from solution import Solution

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
    for k1,k2 in zip(childd,parent2d):
        if isinstance(childd[k1], int) or isinstance(childd[k1], float):
            if random.randint(0,1):
                childd[k1] = (childd[k1] + parent2d[k2]) / 2
            else:
                if random.randint(0,1): # if 1, we change to parent 2... keep otherwise
                    childd[k1] = parent2d[k2]
        if isinstance(childd[k1], dict):
            copulate_recursive(childd[k1], parent2d[k2])

