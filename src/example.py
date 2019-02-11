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
    [-1, -1,  1, -1],
    [ 1,  1, -1, -1]
]

m_te = [
    [-1, -1,  1, -1],
    [-1,  1, -1, -1],
    [ 1, -1, -1, -1],
    [-1, -1, -1,  1]
]

m_st = [
    [ 1,  1,  1,  0],
    [ 0,  1,  0,  0]
]


max_executions = 1
tasks_count = 4
data_entities_count = 4
max_workflow_trace_count = tasks_count * max_executions # 3. The maximum length of the workflow trace

# decision variables
workflow_trace = VarArray(max_workflow_trace_count, tasks_count, 'task')
process_states = Matrix(max_workflow_trace_count, data_entities_count, -1, 1)

last_task_index = Variable(max_workflow_trace_count)

m_tc_var = Matrix(tasks_count, data_entities_count, -1, 1)
m_te_var = Matrix(tasks_count, data_entities_count, -1, 1)


model = Model()

model.add(matrixElements(m_tc_var, m_tc))
model.add(matrixElements(m_te_var, m_te))

# 2. No more than max_execution occurances of task in workflow trace
model.add([Cardinality(workflow_trace, x) <= max_executions for x in range(0, tasks_count)])

# 4. The input state of the first executed task should be equal to s_0
model.add([process_states[0, i] == s_0[i] for i in range(0, data_entities_count)])

# 5. Every non-empty task should change the current state.
def changeState(i):
    task = workflow_trace[i]
    state = process_states[i]
    next_state = process_states[i+1]
    effects = m_te_var[task]
    return Conjunction([
        # Equivalent of:
        # if ((effects[s] == -1) then 
        #   next_state[s] == state[s]
        # else 
        #   next_state[s] == effects[s]
        
        
        # ((effects[s] == -1) and (next_state[s] == state[s])) 
        # or
        # ((effects[s] != -1) and (next_state[s] == effects[s]))


        # ((effects[s] != -1) or (next_state[s] == state[s]))
        # and
        # ((effects[s] ==  -1) or (next_state[s] == effects[s]))

        (not (effects[s] == -1) or (next_state[s] == state[s]))
        and
        (not (effects[s] != -1) or (next_state[s] == effects[s]))

        # next_state[s] == effects[s]

        for s in range(0, data_entities_count)
    ])

# model.add([changeState(i) for i in range(0, max_workflow_trace_count - 1)])

# Helpers

def state_satisfies_requirements(state, requirements):
    if len(state) != len(requirements):
        print(state, len(state))
        print(requirements, len(requirements))
        print(requirements[0])
    assert len(state) == len(requirements)
    return Conjunction([ 
        (state[s] == requirements[s]) or 
        (requirements[s] == -1) 
        for s in range(0, len(state))
    ])

def state_satisfies_requirements_set(state, requirements_set):
    print(state, len(state))
    print(requirements_set, len(requirements_set))
    print(requirements_set[0])
    x = Disjunction([
        state_satisfies_requirements(state, requirements_set[i])
        for i in range(0, len(requirements_set))
    ])
    print(x)
    return x

# 6. The process should end when the desired goal state is achieved.
def process_should_end(i):
    state = process_states[i]
    return (
        # Implication as disjunction
        # p -> q <=> ~p \/ q
        (not state_satisfies_requirements(state, m_st[0]))
        or 
        (last_task_index < (i + 1))
    )

# model.add([process_should_end(i) for i in range(0, max_workflow_trace_count)])


# 7. The last state of the process should satisfy one of the goal states.
last_state = process_states[max_workflow_trace_count - 1]
model.add(state_satisfies_requirements_set(last_state, m_st))


# 8. A task can be executed only if the current state satisfies its input conditions.

def task_condition_check(i):
    task = workflow_trace[i]
    state = process_states[i]
    conditions = m_tc_var[task]
    return state_satisfies_requirements(state, conditions)

model.add([task_condition_check(i) for i in range(0, max_workflow_trace_count)])

solver = model.load('MiniSat')

solver.startNewSearch()

solution_count = 0

solutions = []

def VarArray_to_list(var_array):
    return [x.get_value() for x in var_array]

def Matrix_to_list(matrix):
    return [VarArray_to_list(row) for row in matrix]



while solver.getNextSolution() == SAT:
    solution_count += 1
    print(workflow_trace)
    print(process_states)
    # print(last_task_index)
    #break
    solutions.append((VarArray_to_list(workflow_trace), Matrix_to_list(process_states)))


print(f'Solutions: {solution_count}')



# for s in solutions:
#     workflow_trace = s[0]
#     states = s[1]
#     for i in range(0, len(workflow_trace)):
#         trace = workflow_trace[i]
#         for j in range(0, len(states[i])):
#             if m_tcs[1][]


# print(state_satisfies_requirements_set(VarArray(2, 2), [[0,0],[0,1]]))