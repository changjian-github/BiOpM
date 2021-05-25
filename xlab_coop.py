# -*- coding: utf-8 -*-
"""
method in lab.
"""
import argparse
import json
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import time
from random import sample
# local
from node import MOTS
from util import (
    covered_area_from_front,
    refine,
    tab2str
)


def build_folders(block, n_weight, setting):
    subfolder = 'WS{}-TD{}-RD{}-A{}'.format(n_weight, *setting)
    folders = ['xlab',
               'xlab/coop-blk{}'.format(block),
               'xlab/coop-blk{}/{}'.format(block, subfolder)]
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            pass
        pass
    pass


def worker(cid, jid, name, setting, weights, steps, times, t0,
           CNT, EXT, NDFs, HTBs, HTCs):
    mots = MOTS(cid, name, setting)
    index = np.arange(len(EXT))
    while True:
        if not np.any(EXT):
            mots.initialize(jid, weights[jid])
            mots.start(t0, CNT, EXT, HTBs[jid], HTCs[jid], NDFs[jid])
            times[cid].append([jid, round(mots.duration, 2)])
        elif np.all(EXT):
            break
        else:
            ocp_ids = index[np.array(EXT)==0]
            vac_jid = sample(list(ocp_ids), 1)[0]
            mots.initialize(vac_jid, weights[vac_jid])
            mots.start(t0, CNT, EXT, HTBs[vac_jid], HTCs[vac_jid], NDFs[vac_jid])
            times[cid].append([vac_jid, round(mots.duration, 2)])
        pass
    steps[cid] = mots.local_step
    pass


def run(name, n_weight, setting):
    # prepare
    weights = np.linspace(1, 2*n_weight-1, n_weight) / (2*n_weight)
    cids = jids = list(range(n_weight))
    # process
    CNT = mp.Manager().Array('i', [0]*n_weight)
    EXT = mp.Manager().Array('i', [0]*n_weight)
    HTBs = {i: mp.Manager().dict() for i in range(n_weight)}
    HTCs = {i: mp.Manager().dict() for i in range(n_weight)}
    NDFs = {i: mp.Manager().dict() for i in range(n_weight)}
    steps = mp.Manager().Array('i', [0]*n_weight)
    times = {i: mp.Manager().list() for i in range(n_weight)}
    pool = mp.Pool(processes=n_weight)
    t0 = time.time()
    for cid, jid in zip(cids, jids):
        pool.apply_async(worker,
                         args=[cid, jid, name, setting, weights, steps, times,
                               t0, CNT, EXT, NDFs, HTBs, HTCs])
        pass
    pool.close()
    pool.join()
    # get result
    str_weights = ['{}/{}'.format(2*i+1, 2*n_weight) for i in range(n_weight)]
    steps = list(steps)
    raw_NDF, clock_tab, RSC, SUM = {}, {}, {}, {}
    wall_times = []
    for i, str_weight in enumerate(str_weights):
        raw_NDF.update(dict(NDFs[i]))
        RSC[i] = pd.DataFrame(list(times[i]), columns=['JobID', 'Time'])
        wall_time = list(RSC[i]['Time'])[-1]
        clock_tab[str_weight] = round(wall_time, 2)
        wall_times.append(wall_time)
        pass
    NDF = refine(raw_NDF)
    SUM['area'] = covered_area_from_front(NDF)
    SUM['time'] = round(max(wall_times), 2)
    SUM['size'] = len(NDF)
    SUM['dist'] = clock_tab
    SUM['step'] = sum(steps)
    return NDF, RSC, SUM


def parse_parameters(para):
    # para = "name,n_weight,setting,block"
    str_list = para.split(',')
    name = str_list[0]
    n_weight = eval(str_list[1])
    setting = list(map(eval, str_list[2].split('-')))
    block = eval(str_list[3])
    return name, n_weight, setting, block


def main(args):
    name, n_weight, setting, block = parse_parameters(args.para)
    NDF, RSC, SUM = run(name, n_weight, setting)
    NDF = tab2str(NDF)
    build_folders(block, n_weight, setting)
    subfolder = 'WS{}-TD{}-RD{}-A{}'.format(n_weight, *setting)
    genres = ['NDF', 'SUM']
    tables = [NDF, SUM]
    for genre, table in zip(genres, tables):
        json_file = 'xlab/coop-blk{}/{}/{}-{}.json'.format(
            block, subfolder, name, genre)
        with open(json_file, 'w') as f:
            json.dump(table, f, indent=4)
        pass
    for i in range(n_weight):
        csv_file = 'xlab/coop-blk{}/{}/{}-CPU{}.csv'.format(
            block, subfolder, name, i)
        RSC[i].to_csv(csv_file, index=False)
        pass
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--para', type=str)
    args = parser.parse_args()
    main(args)