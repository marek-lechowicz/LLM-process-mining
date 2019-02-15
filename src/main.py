import os

from os import listdir, makedirs
from os.path import join, exists, basename, splitext
from Numberjack import *
from utilities import *
from workflow_generator import *
from read_input_file import *
from traces_to_csv import *
from pyprom import alpha
from bpmn_generator import build_bpmn

from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.algo.discovery.simple.model.log import factory as simple_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.petri.check_soundness import check_petri_wfnet_and_soundness
from pm4py.objects.conversion.petri_to_bpmn import factory as bpmn_converter
from pm4py.visualization.bpmn import factory as bpmn_vis_factory
from pm4py.objects.bpmn.exporter import bpmn20 as bpmn_exporter



def process_file(input_file):
    print(f'Processing file {input_file}')
    print()
    s_0, m_tc, m_te, m_st, e_t = read_input_file(input_file)

    log = process(s_0, m_tc, m_te, m_st, e_t)

    if not exists('solutions'):
        makedirs('solutions')

    base = basename(input_file)
    name = splitext(base)[0]

    output_file_name = join('solutions', name + '_log.txt')

    with open(output_file_name, 'w+') as file:
        for trace in log:
            file.write(' '.join(trace))
            file.write('\n')

    csv = convert_traces_to_csv(log)

    event_log = csv_importer.import_log_from_string(csv)

    explore_process(name, event_log, alpha_miner, 'alpha_miner')
    explore_process(name, event_log, inductive_miner, 'inductive_miner')
    explore_process(name, event_log, simple_miner, 'simple_miner')


def explore_process(name, event_log, miner, miner_name):
    net, initial_marking, final_marking = miner.apply(event_log)

    bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_converter.apply(net, initial_marking, final_marking)

    bpmn_exporter.export_bpmn(bpmn_graph, join('solutions', name + '_' + miner_name + '.bpmn'))
    bpmn_figure = bpmn_vis_factory.apply(bpmn_graph)
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.png'))



def process(s_0, m_tc, m_te, m_st, e_t):
    print('Initial state:')
    print(s_0)
    print('Task conditions:')
    print(m_tc)
    print('Task effects:')
    print(m_te)
    print('Goal states:')
    print(m_st)
    print('Max task executions:')
    print(e_t)
    print('----------------------------------------------------------')

    model, workflow_trace, process_states, last_task_index = get_model(
        s_0, m_tc, m_te, m_st, e_t)

    # solver = model.load('Gecode')
    solver = model.load('Mistral')
    # solver = model.load('Mistral2')

    solver.startNewSearch()

    solutions = []

    print('Solutions:')
    print('==========')
    while solver.getNextSolution() == SAT:
        print(workflow_trace)
        print(process_states)
        print(last_task_index)
        solutions.append((
            VarArray_to_list(workflow_trace),
            Matrix_to_list(process_states),
            last_task_index.get_value()))
        print('----------')

    print()
    print(f'Solutions count: {len(solutions)}')
    print('==========================================================')
    print()

    log = []
    for s in solutions:
        trace, _, last = s
        trace = trace[0:last]
        trace = list(map(lambda x: chr(64 + x), trace))
        log.append(trace)
        print(trace)

    print()
    print()

    return log


if __name__ == "__main__":
    for file in listdir('problems'):
        if splitext(file)[1] == '.txt':
            process_file(join('problems', file))
