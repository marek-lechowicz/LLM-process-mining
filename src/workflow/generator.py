from Numberjack import *
from workflow.constraint_model import get_model
from workflow.utilities import *

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