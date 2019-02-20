from Numberjack import *
from workflow.utilities import *


def get_model(s_0, m_tc, m_te, m_st, e_t):
    assert len(m_tc) == len(m_te)
    for row in m_tc:
        assert len(row) == len(s_0)
    for row in m_te:
        assert len(row) == len(s_0)
    for row in m_st:
        assert len(row) == len(s_0)

    # Add dummy task at '0' position
    m_tc = [[-1 for i in range(0, len(m_tc[0]))]] + m_tc
    m_te = [[-1 for i in range(0, len(m_te[0]))]] + m_te

    e_t = [0] + e_t

    max_executions = 2
    tasks_count = len(m_tc)
    data_entities_count = len(s_0)
    max_workflow_trace_count = tasks_count * max_executions

    workflow_trace = VarArray(max_workflow_trace_count, tasks_count, 'task')
    process_states = Matrix(max_workflow_trace_count,
                            data_entities_count, 0, 1, 'state')

    last_task_index = Variable(max_workflow_trace_count, 'last_task_index')

    model = Model()

    # As we want to use m_tc and m_te rows selected by variable we have to
    # create variable matrix (m_tc_var, m_te_var) and bind it's elements
    # to corresponding values from m_tc and m_te.
    m_tc_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_tc')
    m_te_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_te')
    model.add(matrixElements(m_tc_var, m_tc))
    model.add(matrixElements(m_te_var, m_te))


    # Helpful predicates

    def state_satisfies_requirements(state, requirements):
        return Conjunction([
            (state[s] == requirements[s]) | (requirements[s] == -1)
            for s in range(0, len(state))
        ])

    def state_satisfies_requirements_set(state, requirements_set):
        return Disjunction([
            state_satisfies_requirements(state, requirements_set[i])
            for i in range(0, len(requirements_set))
        ])


    # Tasks should not repeat
    # model.add(AllDiffExcept0(workflow_trace)) 


    # Count of occurences for each task should be lower or equal to it's value from e_t or to max_executions
    model.add([
        Cardinality(workflow_trace, i) <= ( e_t[i] if (e_t[i] > 0) and (e_t[i] < max_executions) else max_executions )
        for i in range(1, tasks_count)])

    
    # Last task in workflow trace shoud be dummy task
    model.add(workflow_trace[max_workflow_trace_count - 1] == 0)


    # First state should be equal to the defined state
    model.add([process_states[0, i] == s_0[i] for i in range(0, data_entities_count)])

    
    # The last task index should not be preceeded by any idle task
    # also all tasks after it should be idle
    def constraint_idle_tasks(i):
        return (last_task_index <= i) == (workflow_trace[i] == 0)

    model.add([constraint_idle_tasks(i) for i in range(0, max_workflow_trace_count)])


    # End process when any desired goal is achieved
    def process_should_end(i):
        state = process_states[i]
        return state_satisfies_requirements_set(state, m_st) == (workflow_trace[i] == 0)
                
    model.add([process_should_end(i) for i in range(0, max_workflow_trace_count)])


    # The last state of the process should satisfy any desired goal
    last_state = process_states[max_workflow_trace_count - 1]
    model.add(state_satisfies_requirements_set(last_state, m_st))


    # Every task can be only executed when state satisfies its conditions
    def task_condition_check(i):
        task = workflow_trace[i]
        state = process_states[i]
        conditions = m_tc_var[task]
        return state_satisfies_requirements(state, conditions)

    model.add([task_condition_check(i) for i in range(0, max_workflow_trace_count)])


    # Every state has to be changed according to the executed task, otherwise it should not change 
    def constraint_next_state(i):
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
            #
            # Implication as disjunction:
            # p -> q <=> ~p \/ q
            #
            # so:
            # p -> q /\ ~p -> r <=> (~p \/ q) /\ (p \/ r)

            ((effects[s] != -1) | (next_state[s] == state[s]))
            &
            ((effects[s] == -1) | (next_state[s] == effects[s]))

            for s in range(0, data_entities_count)
        ])

    model.add([constraint_next_state(i) for i in range(0, max_workflow_trace_count - 1)])    


    return (
        model,
        workflow_trace,
        process_states,
        last_task_index
    )
