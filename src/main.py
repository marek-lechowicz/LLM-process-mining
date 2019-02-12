from os import listdir, makedirs
from os.path import join, exists, basename, splitext
from Numberjack import *
from utilities import *
from workflow_generator import *
from read_input_file import *
from pyprom import alpha


def process_file(input_file):
    print(f'Processing file {input_file}')
    print()
    s_0, m_tc, m_te, m_st = read_input_file(input_file)

    log = process(s_0, m_tc, m_te, m_st)

    if not exists('solutions'):
        makedirs('solutions')

    base = basename(input_file)
    name = splitext(base)[0]

    output_file_name = join('solutions', name + '_out.txt')

    with open(output_file_name, 'w+') as file:
        for trace in log:
            file.write(trace)
            file.write('\n')

    alpha.apply(log, '', join('solutions', name))


def process(s_0, m_tc, m_te, m_st):
    print('Initial state:')
    print(s_0)
    print('Task conditions:')
    print(m_tc)
    print('Task effects:')
    print(m_te)
    print('Goal states:')
    print(m_st)
    print('----------------------------------------------------------')

    model, workflow_trace, process_states, last_task_index = get_model(
        s_0, m_tc, m_te, m_st)

    # solver = model.load('MiniSat')
    # solver = model.load('WalkSat')
    solver = model.load('Mistral')

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
        trace = ' '.join(map(lambda x: chr(64 + x), trace))
        log.append(trace)
        print(trace)

    print()
    print()

    return log


if __name__ == "__main__":
    for file in listdir('problems'):
        process_file(join('problems', file))
