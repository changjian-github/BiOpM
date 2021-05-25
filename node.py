# -*- coding: utf-8 -*-
"""
A new file.
"""
import time
from random import sample
# local
from algo import variable_global_search
from util import (
    extract_dataset,
    weighted_sum_objective
)


class MOTS:
    def __init__(self, cid, name, setting):
        self.cid = cid
        data1, data2, level = extract_dataset(name)
        self.data1 = data1
        self.data2 = data2
        self.dim = data1.shape[1]
        self.level = level
        self.tabu_depth = setting[0]
        self.remain_depth = setting[1]
        self.alpha = setting[2]
        self.local_step = 0
        self.jump_range = self.alpha * min(level, data1.shape[1] - level)
    def initialize(self, jid, weight):
        self.jid = jid
        self.weight = weight
    def start(self, t0, CNT, EXT, HTB, HTC, NDF):
        init_sol = tuple(sorted(sample(range(self.dim), self.level)))
        init_obj = weighted_sum_objective(
            self.data1, self.data2, init_sol, self.weight)
        variable_global_search(self, init_sol, init_obj, CNT, EXT, HTB, HTC, NDF)
        self.duration = time.time() - t0
    pass
