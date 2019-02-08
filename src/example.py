from Numberjack import *

def matrixElements(matrix_var, matrix):
    assert len(matrix) == len(matrix_var)
    assert len(matrix) > 0
    assert len(matrix[0]) == len(matrix_var[0])

    constraints = []

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            constraints.append(matrix_var[i][j] == matrix[i][j])
    return constraints

s_0 = [0, 0, 0, 0]

m_tc = [
    [ 0,  0,  0,  0],
    [-1, -1,  1, -1],
    [-1,  1, -1, -1]
]

m_te = [
    [-1, -1,  1, -1],
    [-1,  1, -1, -1],
    [ 1, -1, -1, -1]
]

m_st = [
    [ 1, -1, -1, -1]
]


max_executions = 2
tasks_count = 3
data_entities_count = 4
max_workflow_trace_count = tasks_count * max_executions

# decision variables
workflow_trace = VarArray(max_workflow_trace_count, 1, tasks_count, 'task')
process_states = Matrix(max_workflow_trace_count, data_entities_count, -1, 2)

last_task_index = Variable(max_workflow_trace_count)




model = Model()

model.add(matrixElements(m_tc_var, m_tc))

# No more than max_execution occurances of task in workflow trace
model.add([Cardinality(workflow_trace, x) <= max_executions for x in range(1, tasks_count + 1)])

# The input state of the first executed task should be equal to s_0
model.add([process_states[0, i] == s_0[i] for i in range(0, data_entities_count)])

def changeState(i):
    task = workflow_trace[i]
    state = process_states[i]
    next_state = process_states[i+1]
    effects = VarArray(data_entities_count, -1, 2)
    effects_constraints = [effects[s] == m_te_var[task, s] for s in range(0, data_entities_count)]
    [  for s in range(0, data_entities_count)]

model.add([])




solver = model.load('MiniSat')

solver.startNewSearch()

while solver.getNextSolution() == SAT:
    print([x.get_value() for x in workflow_trace])
