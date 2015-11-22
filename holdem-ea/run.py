import argparse
import os
from ea import EA

parser = argparse.ArgumentParser(description="Texas holdem bot EA")
parser.add_argument('--config', type=argparse.FileType('r', 0), default=os.path.abspath("../config_starter.json"))

args = parser.parse_args()

#ea = EA(64, 32, 10, 10, args.config)
ea = EA(16, 4, 2, 10, args.config)
ea.run()

print("\n\n")
for s in sorted(ea.this_generation.population, key=lambda p: p.fitness):
    print("{0} {1} {2}\n    {3}\n".format(s.fitness, s.wins, s.losses, s.get_config_file()))
