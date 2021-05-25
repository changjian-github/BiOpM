# -*- coding: utf-8 -*-
"""
A new file.
"""
import json
import numpy as np
import os
import subprocess
from itertools import product


def build_folders():
    folders = ['logs',
               'logs/output',
               'logs/error',
               'submit']
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            pass
        pass
    pass


# change parameters here
def combine_parameters(blocks, names, n_weights, settings):
    paras = []
    for block, name, n_weight, setting in product(blocks, names, n_weights, settings):
        para = '{},{},{}-{}-{},{}'.format(name, n_weight, *setting, block)
        paras.append(para)
        pass
    return paras


def load_names(genre):
    file = 'name-table.json'
    with open(file, 'r') as f:
        name_table = json.load(f)
    names = name_table[genre]
    return names


def string_arguments(paras, script):
    arguments = []
    for para in paras:
        argument = '--para {}'.format(para)
        arguments.append(argument)
        pass
    return arguments


def string_job_array(arguments, job, script):
    txt = ('#!/bin/sh\n'
           '#PBS -M cmjdxy@foxmail.com\n'
           '#PBS -m abe\n'
           '#PBS -N {0}\n'
           '#PBS -l ncpus=1\n'
           '#PBS -l partition=su02\n'
           '#PBS -l walltime=120:00:00\n'
           '#PBS -o logs/output/{0}.o\n'
           '#PBS -e logs/error/{0}.e\n'
           '#PBS -t 0-{1}\n\n'
           'cd $PBS_O_WORKDIR\n\n').format(job, len(arguments)-1)
    txt += 'ARGS=(\n'
    for argument in arguments:
        txt += '    "{}"\n'.format(argument)
        pass
    txt += (')\n\n'
            'python %s ${ARGS[$PBS_ARRAYID]}\n') % script
    return txt


def write_shell(job, paras, script, shell):
    build_folders()
    arguments = string_arguments(paras, script)
    string = string_job_array(arguments, job, script)
    with open(shell, 'w') as f:
        f.write(string)
    pass


def func():
    method = 'coop'
    names = load_names('sample')
#    names = ['pmed17-p25']
    n_weights = [8]
    settings = [[10, 800, 1]]
    blocks = list(range(10))
    build_folders()
    paras = combine_parameters(blocks, names, n_weights, settings)
    shell = 'submit-{}.pbs'.format(method)
    script = 'xlab_{}.py'.format(method)
    write_shell(method, paras, script, shell)
    resp = subprocess.run(['dos2unix', shell],
                          capture_output=True,
                          encoding='gbk')
    print(resp.stderr)
    pass


def main():
    func()

    pass


if __name__ == '__main__':
    main()
    pass