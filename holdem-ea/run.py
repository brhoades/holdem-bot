import argparse
import os
from ea import EA

parser = argparse.ArgumentParser(description="Texas holdem bot EA")
parser.add_argument('--config', type=argparse.FileType('r', 0), default=os.path.abspath("../config_starter.json"))

args = parser.parse_args()

ea = EA(100, 50, 100, 10, args.config)
ea.run()
