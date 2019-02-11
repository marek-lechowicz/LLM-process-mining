from Numberjack import *
from utilities import *


def get_model(s_0, m_tc, m_te, m_st):
    assert len(m_tc) == len(m_te)
    for row in m_tc:
        assert len(row) == len(s_0)
    for row in m_te:
        assert len(row) == len(s_0)
    for row in m_st:
        assert len(row) == len(s_0)

    max_executions = 1
    tasks_count = len(m_tc)
    data_entities_count = len(s_0)
    # 3. The maximum length of the workflow trace
    max_workflow_trace_count = tasks_count * max_executions

    # decision variables
    workflow_trace = VarArray(max_workflow_trace_count, tasks_count, 'task')
    process_states = Matrix(max_workflow_trace_count,
                            data_entities_count, -1, 1, 'state')

    last_task_index = Variable(max_workflow_trace_count)

    model = Model()

    # As we want to use m_tc and m_te rows selected by variable we have to
    # create variable matrix (m_tc_var, m_te_var) and bind it's elements
    # to corresponding values from m_tc and m_te.
    m_tc_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_tc')
    m_te_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_te')
    model.add(matrixElements(m_tc_var, m_tc))
    model.add(matrixElements(m_te_var, m_te))

    # 2. No more than max_execution occurances of task in workflow trace
    model.add([
        Cardinality(workflow_trace, x) <= max_executions
        for x in range(0, tasks_count)])

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
        return Conjunction([
            # Equivalent of:
            # if ((effects[s] == -1) then
            #   next_state[s] == state[s]
            # else
            #   next_state[s] == effects[s]
            #
            # Implication as disjunction
            # p -> q <=> ~p \/ q

            ((effects[s] != -1) | (next_state[s] == state[s]))
            &
            ((effects[s] == -1) | (next_state[s] == effects[s]))

            for s in range(0, data_entities_count)
        ])

    model.add([change_state(i)
               for i in range(0, max_workflow_trace_count - 1)])

    # Helpers

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

    # 6. The process should end when the desired goal state is achieved.

    def process_should_end(i):
        state = process_states[i]
        return (
            # Implication as disjunction
            # p -> q <=> ~p \/ q
            (not state_satisfies_requirements(state, m_st[0]))
            |
            (last_task_index < (i + 1))
        )

    model.add([process_should_end(i)
               for i in range(0, max_workflow_trace_count)])

    # 7. The last state of the process should satisfy one of the goal states.
    last_state = process_states[max_workflow_trace_count - 1]
    model.add(state_satisfies_requirements_set(last_state, m_st))

    # 8. A task can be executed only if the current state satisfies its input conditions.

    def task_condition_check(i):
        task = workflow_trace[i]
        state = process_states[i]
        conditions = m_tc_var[task]
        return state_satisfies_requirements(state, conditions)

    model.add([task_condition_check(i)
               for i in range(0, max_workflow_trace_count)])

    return (
        model,
        workflow_trace,
        process_states,
        last_task_index
    )
