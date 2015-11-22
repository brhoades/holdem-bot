import random
import json
import copy
import md5
import os

class Solution(object):
    def __init__(self, data, perturb):
        self.data = copy.deepcopy(data)
        self.digest = None
        self.times = []

        self.wins   = 0
        self.losses = 0
        
        # make our data interesting
        self.perturb(self.data, perturb)
        self.update_hash()

    def perturb(self, d, perturb):
        for k in d:
            if isinstance(d[k], int) or isinstance(d[k], float):
                d[k] *= random.random() * perturb
            if isinstance(d[k], dict):
                self.perturb(d[k], perturb)
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
