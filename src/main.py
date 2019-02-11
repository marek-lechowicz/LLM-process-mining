from Numberjack import *
from utilities import *
from generator import *

s_0 = [0, 0, 0, 0]

m_tc = [
    [0,  0,  0,  0],
    [-1, -1,  1, -1],
    [-1, -1,  1, -1],
    [1,  1, -1, -1],
    [-1, -1, -1,  0]
]

m_te = [
    [-1, -1,  1, -1],
    [-1,  1, -1, -1],
    [1, -1, -1, -1],
    [-1, -1, -1,  1],
    [-1, -1, -1,  1]
]

m_st = [
    [1,  1,  1,  0],
    [0,  1,  0,  0],
    [-1, -1, -1,  1]
]

model = get_model(s_0, m_tc, m_te, m_st)

# solver = model.load('MiniSat')
# solver = model.load('WalkSat')
solver = model.load('Mistral')

solver.startNewSearch()

solution_count = 0

solutions = []

while solver.getNextSolution() == SAT:
    solution_count += 1
    print(workflow_trace)
    print(process_states)
    print(last_task_index)
    solutions.append((VarArray_to_list(workflow_trace),
                      Matrix_to_list(process_states)))

print(f'Solutions: {solution_count}')
