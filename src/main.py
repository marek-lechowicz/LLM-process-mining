import os

from os import listdir, makedirs
from os.path import join, exists, basename, splitext, dirname

from workflow.generator import get_workflow_log
from process_discovery.code import explore_process
from utils import get_task_names, name_tasks, convert_traces_to_csv
from parser import *

from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner


def process_file(input_file):
    print(f'Processing file {input_file}')
    print()

    s_0, m_tc, m_te, m_st, e_t = read_input_file(input_file)

    task_names = get_task_names(input_file, len(m_tc))

    workflow_log = get_workflow_log(s_0, m_tc, m_te, m_st, e_t)

    log = name_tasks(workflow_log, task_names)

    if not exists('solutions'):
        makedirs('solutions')

    base = basename(input_file)
    name = splitext(base)[0]

    log_output_file_name = join('solutions', name + '_log.txt')

    output_log = []
    for trace in log:
        quoted_trace = map(lambda x: '"' + x + '"', trace)
        comma_separated_trace = ', '.join(quoted_trace)
        output_log.append(comma_separated_trace)
    
    output_log.sort()

    with open(log_output_file_name, 'w+') as file:
        file.write('\n'.join(output_log))
        

    csv = convert_traces_to_csv(log)

    csv_log_output_file_name = join('solutions', name + '_log.csv')

    with open(csv_log_output_file_name, 'w+') as file:
        file.write(csv)

    explore_process(name, csv, alpha_miner, 'alpha_miner')
    explore_process(name, csv, inductive_miner, 'inductive_miner')





if __name__ == "__main__":
    for file in listdir('problems'):
        if splitext(file)[1] == '.txt':
            process_file(join('problems', file))
