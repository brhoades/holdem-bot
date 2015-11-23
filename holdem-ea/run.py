import argparse
import os
from ea import EA

parser = argparse.ArgumentParser(description="Texas holdem bot EA")
parser.add_argument('--config', type=argparse.FileType('r', 0), default=os.path.abspath("../config_starter.json"))

args = parser.parse_args()

ea = EA(64, 32, 10000, 10, args.config)
#ea = EA(16, 8, 6, 10, args.config)
ea.run()

print("\n\n")
print("Age\tFit\tWin\tLoss\tTime")
for s in sorted(ea.this_generation.population, key=lambda p: p.fitness, reverse=True):
    print("{0}\t{1}\t{2}\t{3}\t{4}\n    {5}\n".format(s.generation, round(s.fitness), s.wins, s.losses, \
        s.average_time, s.get_config_file()))
