import random
import json
import copy
import md5
import os

class Solution(object):
    def __init__(self, data, gen, perturb=None):
        self.data = copy.deepcopy(data)
        self.digest = None
        self.times = []

        self.wins   = 0
        self.losses = 0

        self.generation = gen
        
        # make our data interesting
        if perturb is not None:
            self.perturb(self.data, perturb)
            self.update_hash()

    def perturb(self, d, perturb):
        for k in d:
            if isinstance(d[k], int) or isinstance(d[k], float):
                d[k] *= random.random() * perturb
            if isinstance(d[k], dict):
                self.perturb(d[k], perturb)

    def mutate(self, d=None):
        if d is None:
            d = self.data
        for k in d:
            if isinstance(d[k], int) or isinstance(d[k], float):
                i = random.randint(0,9)
                if i <= 3:
                    # can be completely transformed
                    d[k] *= random.random()
                elif i == 4:
                    # or increased
                    d[k] += random.random()
                elif i == 5:
                    # or decreased
                    d[k] -= random.random()
                #otherwise we leave it alone.
                # that works out to 10% (default rate) of children
                # wading through nuclear waste and 1 in 2 of their attributes
                # being changed

            if isinstance(d[k], dict):
                self.mutate(d[k])

    def update_hash(self, data=None):
        m = md5.new()
        if data is None:
            m.update(json.dumps(self.data))
        else:
            m.update(data)

        self.digest = m.hexdigest()
    
    def get_config_file(self):
        f = "/tmp/holdemeahashes/"
        if not os.path.exists(f):
            os.mkdir(f)
        f = os.path.abspath(os.path.join(f, self.digest+".json"))
        if not os.path.exists(f):
            with open(f, 'wb') as fp:
                json.dump(self.data, fp)
        return f

    def get_command(self):
        return "python2 ../bot.py --no-log --use-eval --config {0}".format(self.get_config_file())

    @property
    def fitness(self):
        if self.losses == 0 and self.wins > 0:
            return self.wins
        elif self.losses == 0:
            return 0
        return float(self.wins) / self.losses

    @property
    def average_time(self):
        if len(self.times) == 0:
            return 1000
        return sum(self.times)/len(self.times)

