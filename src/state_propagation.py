from Numberjack import *
from utilities import *

s_0 = [0, 0, 0, 0]

m_te = [
    [-1, -1,  1, -1],
    [-1,  1, -1, -1],
    [ 1, -1, -1, -1],
    [-1, -1, -1,  1]
]

max_executions = 1
tasks_count = 4
data_entities_count = 4
max_workflow_trace_count = tasks_count * max_executions # 3. The maximum length of the workflow trace

workflow_trace = VarArray(max_workflow_trace_count, tasks_count, 'task')
process_states = Matrix(max_workflow_trace_count, data_entities_count, -1, 1, 'state')



m_te_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_te')

model = Model()

model.add(matrixElements(m_te_var, m_te))
model.add(varArrayElements(workflow_trace, [0,1,2,3]))

# 4. The input state of the first executed task should be equal to s_0
model.add([
    process_states[0, i] == s_0[i] 
    for i in range(0, data_entities_count)])

# 5. Every non-empty task should change the current state.
def change_state(i):
    task = workflow_trace[i]
    state = process_states[i]
    next_state = process_states[i+1]
    effects = m_te_var[task]
    return [
        # Equivalent of:
        # if ((effects[s] == -1) then 
        #   next_state[s] == state[s]
        # else 
        #   next_state[s] == effects[s]

        # ((effects[s] != -1) or (next_state[s] == state[s]))
        # and
        # ((effects[s] ==  -1) or (next_state[s] == effects[s]))

        # And([
        #     Or([(effects[s] != -1), (next_state[s] == state[s])]),
        #     Or([(effects[s] == -1), (next_state[s] == effects[s])]),
        # ])

        ((effects[s] != -1) | (next_state[s] == state[s]))
        &
        ((effects[s] ==  -1) | (next_state[s] == effects[s]))

        for s in range(0, data_entities_count)
    ]

model.add([change_state(i) for i in range(0, max_workflow_trace_count - 1)])



solver = model.load('MiniSat')
# solver = model.load('WalkSat')
# solver = model.load('Mistral')

solver.startNewSearch()

solution_count = 0

solutions = []


while solver.getNextSolution() == SAT:
    solution_count += 1
    print(workflow_trace)
    print(process_states)
    # print(last_task_index)
    #break
    solutions.append((VarArray_to_list(workflow_trace), Matrix_to_list(process_states)))


print(f'Solutions: {solution_count}')

