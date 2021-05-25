# -*- coding: utf-8 -*-
"""
A new file.
"""
import numpy as np
import os
import pandas as pd
import time


def covered_area(pnts):
    sort_index = np.argsort(pnts[:, 0])
    sort_pnts = pnts[sort_index]
    x_coords = sort_pnts[:, 0]
    shift_x_coords = np.array([0] + x_coords[0:-1].tolist())
    y_coords = sort_pnts[:, 1]
    area = np.sum((x_coords - shift_x_coords) * y_coords)
    return area


def covered_area_from_front(front):
    if front:
        pnts = np.array(list(front.keys()))
        area = covered_area(pnts)
    else:
        area = 0
    return area


def detect_front_index(data):
    # dominating relation
    D = dominant_matrix(data)
    cond = np.all(D>=0, axis=1)
    index = list(np.where(cond)[0])
    return index


def dominant_matrix(data):
    n = data.shape[0]
    D = np.zeros([n, n], dtype=np.int8)
    for i in range(0, n-1):
        for j in range(i, n):
            D[i][j] = dominant_relation(data[i], data[j])
            pass
        pass
    D = D - D.T
    return D


def dominant_relation(A, B):
    d = {-1:0, 0:0, 1:0}
    for a, b in zip(A, B):
        if a < b:
            d[-1] += 1
        elif a > b:
            d[1] += 1
        else:
            d[0] += 1
        pass
    if d[-1] > 0 and d[1] == 0:
        r = -1
    elif d[1] > 0 and d[-1] == 0:
        r = 1
    else:
        r = 0
    return r


def extract_dataset(name):
    file1 = 'data/interact/{}.csv'.format(name)
    file2 = 'data/facility/{}.csv'.format(name)
    data1 = pd.read_csv(file1, index_col=0).values
    data2 = pd.read_csv(file2, index_col=0).values
    np.fill_diagonal(data2, 1000) # max: 124.0, name: pmed32-p43
    level = eval(name.split('-')[1][1:])
    return data1, data2, level


def front_updator(front, duo):
    # front = {pnt: sol}
    new_pnt, new_sol = duo
    if new_pnt not in front:
        flag = True
        drop_pnts = []
        for pnt in front.keys():
            if dominant_relation(new_pnt, pnt) == -1:
                flag = False
                break
            elif dominant_relation(new_pnt, pnt) == 1:
                drop_pnts.append(pnt)
            else:
                pass
            pass
        if drop_pnts:
            for pnt in drop_pnts:
                front.pop(pnt)
                pass
        if flag:
            front.update([duo])
    else:
        pass
    pass


def get_coords(data1, data2, sol):
    obj1 = sum(np.min(data1[:, sol], axis=1))
    obj2 = sum(np.min(data2[:, sol][sol, :], axis=1))
    point = (obj1, obj2)
    return point


def is_dominated_by_group(curr_pnt, sort_FPs):
    flag = False
    for FP in sort_FPs:
        if dominant_relation(curr_pnt, FP.pnt) == -1:
            flag = True
            break
        pass
    return flag


def refine(table):
    pnts = np.array(list(table.keys()))
    front_index = detect_front_index(pnts)
    front_pnts = pnts[front_index]
    sort_index = np.argsort(front_pnts[:, 0])
    sort_pnts = front_pnts[sort_index]
    front = dict([(tuple(pnt), table[tuple(pnt)]) for pnt in sort_pnts])
    return front


def tab2eval(table):
    new_table = {}
    for key, value in table.items():
        new_table[eval(key)] = eval(value)
    return new_table


def tab2str(table):
    new_table = {}
    for key, value in table.items():
        new_table[str(key)] = str(value)
        pass
    return new_table


def timeit(func):
    def wrapper(*args, **kw):
        t = time.clock()
        r = func(*args, **kw)
        print('"{}" cost {:.1f}s'.format(func.__name__, time.clock()-t))
        return r
    return wrapper


def timer_updator(table, trio):
    # table = {pnt: (hitT, weight)}
    new_pnt, new_hitT, new_weight = trio
    if new_pnt in table:
        hitT, weight = table[new_pnt]
        if new_hitT < hitT:
            table[new_pnt] = (new_hitT, new_weight)
        else:
            pass
    else:
        table[new_pnt] = (new_hitT, new_weight)
        pass
    pass


def traverse(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_list.append(root + '/' + file)
    return file_list


def weighted_sum_objective(data1, data2, sol, weight):
    obj1 = sum(np.min(data1[:, sol], axis=1))
    obj2 = sum(np.min(data2[:, sol][sol, :], axis=1))
    w_sum = weight*obj1 + (1-weight)*obj2
    return w_sum


def weighted_sum_objective_uniform(data1, data2, minimax, sol, weight):
    max_F1, max_F2, min_F1, min_F2 = minimax
    obj1 = sum(np.min(data1[:, sol], axis=1))
    obj2 = sum(np.min(data2[:, sol][sol, :], axis=1))
    w_sum = weight*(obj1-min_F1)/(max_F1-min_F1) + (1-weight)*(obj2-min_F2)/(max_F2-min_F2)
    return w_sum
