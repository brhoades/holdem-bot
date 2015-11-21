import random
import copy
import json

class Solution(object):
    def __init__(self, data, perturb):
        self.data = copy.deepcopy(data)
        self.fit  = 0
        
        # make our data interesting
        self.perturb(self.data, perturb)

        print(json.dumps(self.data))

    def perturb(self, d, perturb):
        for k in d:
            if isinstance(d[k], int) or isinstance(d[k], float):
                d[k] *= random.random() * perturb
            if isinstance(d[k], dict):
                self.perturb(d[k], perturb)

