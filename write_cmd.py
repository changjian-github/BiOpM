# -*- coding: utf-8 -*-
"""
A new file.
"""
import json
import numpy as np
import os
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
    for block, n_weight, setting, name in product(blocks, n_weights, settings, names):
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
    commands = ['python {} {}'.format(script, argument) for argument in arguments]
    txt = '::<task {}>\n'.format(job)
    txt += '\n'.join(commands)
    txt += '\n\npause'
    return txt


def write_shell(job, paras, script, shell):
    arguments = string_arguments(paras, script)
    string = string_job_array(arguments, job, script)
    with open(shell, 'w') as f:
        f.write(string)
    pass


def func():
    method = 'coop'
    names = load_names('sample')
#    names = ['pmed17-p25'] # for testing
    n_weights = [8]
    A = np.linspace(0.2, 1, 5)
    settings = [[10, 400, round(a, 1)] for a in A]
    blocks = [0]
    build_folders()
    paras = combine_parameters(blocks, names, n_weights, settings)
    shell = 'submit-{}.bat'.format(method)
    script = 'xlab_{}.py'.format(method)
    write_shell(method, paras, script, shell)
    pass


def main():
    func()

    pass


if __name__ == '__main__':
    main()
    pass