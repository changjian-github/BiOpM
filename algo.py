# -*- coding: utf-8 -*-
"""
A new file.
"""
import numpy as np
from random import sample
# local
from nbh import (
    tabu_neighbor_back2current,
    tabu_neighbor_current2back
)
from util import (
    front_updator,
    get_coords,
    weighted_sum_objective
)


# =============================================================================
# tabu search
# =============================================================================
def weighted_tabu_search(self, init_sol, init_obj, CNT, EXT, HTB, HTC, NDF):
    best_sol, best_obj = init_sol, init_obj
    curr_sol, curr_obj = init_sol, init_obj
    ckpt0 = NDF.copy()
    count = 0
    while True:
        if EXT[self.jid]:
            break
        # delete-add
        back_sol, back_obj = _search_current2back(self, curr_sol, HTB)
        if not back_obj:
            break
        curr_sol, curr_obj = _search_back2current(self, back_sol, HTC)
        if not curr_obj:
            break
        # tabu condition
        if curr_obj > best_obj:
            best_sol = curr_sol
            best_obj = curr_obj
            count = 0
        else:
            count += 1
        if count >= self.tabu_depth:
            break
        # global condition
        curr_pnt = get_coords(self.data1, self.data2, curr_sol)
        front_updator(NDF, (curr_pnt, curr_sol))
        ckpt1 = NDF.copy()
        if ckpt1 != ckpt0:
            CNT[self.jid] = 0
        else:
            CNT[self.jid] += 1
        if CNT[self.jid] >= self.remain_depth:
            EXT[self.jid] = 1
        # update
        self.local_step += 1
        ckpt0 = ckpt1.copy()
        pass
    return best_sol, best_obj


def _search_current2back(self, curr_sol, HTB):
    c2b_sols = tabu_neighbor_current2back(curr_sol, HTB)
    if c2b_sols:
        c2b_objs = np.array(
            [weighted_sum_objective(self.data1, self.data2, c2b_sol, self.weight)
             for c2b_sol in c2b_sols]
        )
        c2b_midx = np.argmax(c2b_objs)
        back_sol = c2b_sols[c2b_midx]
        back_obj = c2b_objs[c2b_midx]
        HTB[hash(back_sol)] = 1
    else:
        back_sol = (0, ) * (self.level - 1)
        back_obj = 0
    return back_sol, back_obj


def _search_back2current(self, back_sol, HTC):
    b2c_sols = tabu_neighbor_back2current(self.dim, back_sol, HTC)
    if b2c_sols:
        b2c_objs = np.array(
            [weighted_sum_objective(self.data1, self.data2, b2c_sol, self.weight)
             for b2c_sol in b2c_sols]
        )
        b2c_midx = np.argmax(b2c_objs)
        curr_sol = b2c_sols[b2c_midx]
        curr_obj = b2c_objs[b2c_midx]
        HTC[hash(curr_sol)] = 1
    else:
        curr_sol = (0, ) * self.level
        curr_obj = 0
    return curr_sol, curr_obj


# =============================================================================
# global search
# =============================================================================
def variable_global_search(self, init_sol, init_obj, CNT, EXT, HTB, HTC, NDF):
    # head
    best_sol, best_obj = weighted_tabu_search(
        self, init_sol, init_obj, CNT, EXT, HTB, HTC, NDF)
    paraconfig = 'TD: {}, RD:{}, A:{}, W: {}'.format(
        self.tabu_depth, self.remain_depth, self.alpha, self.weight)
    print(paraconfig)
    jump_num = 2 # solution is 1-NN optimal, jump_num should be 2 at least.
    # body
    while True:
        print('scanning at {}-NN...'.format(jump_num))
        if EXT[self.jid]:
            break
        # perturb
        res = set(range(self.dim)) - set(best_sol)
        temp_sol = _perturb(res, best_sol, jump_num)
        temp_obj = weighted_sum_objective(
            self.data1, self.data2, temp_sol, self.weight)
        # tabu
        stag_sol, stag_obj = weighted_tabu_search(
            self, temp_sol, temp_obj, CNT, EXT, HTB, HTC, NDF)
        # condition: better solution found
        if stag_obj > best_obj:
            best_sol = stag_sol
            best_obj = stag_obj
            jump_num = 2
        else:
            jump_num += 1
        # condition: distance too far
        if jump_num >= self.jump_range:
            jump_num = 2
        pass
    pass


def _perturb(res, sol, jump_num):
    outers = sample(set(sol), jump_num)
    inners = sample(set(res), jump_num)
    new_sol = set(list(sol) + inners) - set(outers)
    new_sol = tuple(sorted(new_sol))
    return new_sol