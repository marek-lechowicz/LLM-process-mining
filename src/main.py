import os

from os import listdir, makedirs
from os.path import join, exists, basename, splitext, dirname
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
from pm4py.visualization.petrinet import factory as pn_vis_factory




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


def explore_process(name, csv, miner, miner_name):
    event_log = csv_importer.import_log_from_string(csv)

    net, initial_marking, final_marking = miner.apply(event_log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.png'))
    pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.pdf'))

    bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_converter.apply(net, initial_marking, final_marking)

    bpmn_exporter.export_bpmn(bpmn_graph, join('solutions', name + '_' + miner_name + '.bpmn'))
    bpmn_figure = bpmn_vis_factory.apply(bpmn_graph)
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.png'))
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.pdf'))


def get_workflow_log(s_0, m_tc, m_te, m_st, e_t):
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

    solver = model.load('Mistral')
    # solver = model.load('Mistral2')

    solver.startNewSearch()

    workflow_log = []

    print('Workflow traces:')
    print('================')
    while solver.getNextSolution() == SAT:
        print(workflow_trace)
        print(process_states)
        print(last_task_index)
        workflow_log.append((
            VarArray_to_list(workflow_trace),
            Matrix_to_list(process_states),
            last_task_index.get_value()))
        print('----------')

    print()
    print(f'Workflow trace count: {len(workflow_log)}')
    print('==========================================================')
    print()

    return workflow_log


def name_tasks(log, task_names):
    task_names = ['dummy'] + task_names
    log_with_named_tasks = []
    for s in log:
        trace, _, last = s
        trace = trace[0:last]
        trace = list(map(lambda x: task_names[x], trace))
        log_with_named_tasks.append(trace)
        print(trace)
    return log_with_named_tasks


def get_task_names(input_file, task_count):
    base = basename(input_file)
    name = splitext(base)[0]
    directory = dirname(input_file)
    task_names_file = join(directory, name + '.task_names')
    if exists(task_names_file):
        with open(task_names_file) as file:
            file_contents = file.read().splitlines()
            file_contents = list(map(lambda line: line.strip(), file_contents))
            assert len(file_contents) == task_count
            return file_contents
    else:
        return [chr(65 + i) for i in range(0, task_count)] # [A, B, C, ... ]


if __name__ == "__main__":
    for file in listdir('problems'):
        if splitext(file)[1] == '.txt':
            process_file(join('problems', file))
