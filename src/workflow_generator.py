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

    # Add dummy task at '0' position
    m_tc = [[-1 for i in range(0, len(m_tc[0]))]] + m_tc
    m_te = [[-1 for i in range(0, len(m_te[0]))]] + m_te

    max_executions = 4
    tasks_count = len(m_tc)
    data_entities_count = len(s_0)
    # 3. The maximum length of the workflow trace
    max_workflow_trace_count = tasks_count * max_executions

    # variables
    workflow_trace = VarArray(max_workflow_trace_count, tasks_count, 'task')
    process_states = Matrix(max_workflow_trace_count,
                            data_entities_count, 0, 1, 'state')

    last_task_index = Variable(max_workflow_trace_count)

    model = Model()

    # As we want to use m_tc and m_te rows selected by variable we have to
    # create variable matrix (m_tc_var, m_te_var) and bind it's elements
    # to corresponding values from m_tc and m_te.
    m_tc_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_tc')
    m_te_var = Matrix(tasks_count, data_entities_count, -1, 1, 'm_te')
    model.add(matrixElements(m_tc_var, m_tc))
    model.add(matrixElements(m_te_var, m_te))


    # count of occurences for each task should be lower or equal to max_executions
    model.add([
        Cardinality(workflow_trace, x) <= max_executions
        for x in range(1, tasks_count)])

    
    # Last task in workflow trace shoud be dummy task
    model.add(workflow_trace[last_task_index] == 0)


    # The input state of the first executed task should be equal to s_0
    model.add([
        process_states[0, i] == s_0[i]
        for i in range(0, data_entities_count)])

    
    # The last task index should not be preceeded by any idle task
    # also all tasks after it should be idle
# constraint count_neq(process, dummy_task, last_task_index); %consider last_process_index here
# constraint forall(i in process_indexes)(
#   if i > last_task_index then process[i] == dummy_task
#   else process[i] != dummy_task endif
# );


# End process when the first (desired) goal is achieved - REVISED 2 times for short processes
# constraint forall(i in process_indexes)(
#   let {
#     array[state_indexes] of var 0..1: state = [process_states[i,s] | s in state_indexes]
#   } in
#   state_satisfies_requirements(state, row(goal_states,1)) ->last_task_index < i+2 %corrected to i+2
# );


# The states beggining from last_task_index + 1 shouldn't change 
# constraint forall(i in 2..last_process_index)(
#   (i > last_task_index + 1) 
# -> 
#   forall(s in state_indexes)(
#      process_states[i, s] == process_states[i-1, s]
#   )
# );


# Last state should satisfy goal state
# array[state_indexes] of var 0..1: last_state = [process_states[last_process_index, s] | s in state_indexes];
# constraint state_satisfies_requirements_set(last_state, goal_states);


    # Every task can be only executed when state satisfies its conditions
    # constraint forall(i in process_indexes)(
    #   let {
    #     var tasks_indexes: task = process[i],
    #     array[state_indexes] of var 0..1: state = [process_states[i,s] | s in state_indexes] ,
    #     array[state_indexes] of var -1..1: conditions = [tasks_conditions[task,s] | s in state_indexes] 
    #   } in
    #   state_satisfies_requirements(state, conditions)
    # );

    def task_condition_check(i):
        task = workflow_trace[i]
        state = process_states[i]
        conditions = m_tc_var[task]
        return state_satisfies_requirements(state, conditions)

    model.add([task_condition_check(i)
               for i in range(0, max_workflow_trace_count)])


    # Every state has to be changed according to the executed task, otherwise it should not change (frame problem)
    # constraint forall(i in real_tasks_indexes)(
    #   let {
    #     var tasks_indexes: task = process[i],
    #     array[state_indexes] of var 0..1: state = [process_states[i,s] | s in state_indexes],
    #     array[state_indexes] of var 0..1: next_state = [process_states[i+1,s] | s in state_indexes],
    #     array[state_indexes] of var -1..1: effects = [tasks_effects[task,s] | s in state_indexes] 
    #   } in
    #   forall(s in state_indexes)(
    #     if effects[s] == -1 then next_state[s] == state[s]
    #     else next_state[s] == effects[s] endif
    #   )
    # );

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

    model.add([constraint_next_state(i)
               for i in range(0, max_workflow_trace_count - 1)])

    # Helper predicates

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
        return state_satisfies_requirements_set(state, m_st) == (workflow_trace[i] == 0)
                
    model.add([process_should_end(i)
               for i in range(0, max_workflow_trace_count)])

    

    def prepending_non_zero(i):
        return Conjunction([
            workflow_trace[j] != 0
            for j in range(0, i)
        ])
    # model.add([ 
    #     (last_task_index == i) == (prepending_non_zero(i)) 
    #     for i in range(1, max_workflow_trace_count)
    # ])

    # 7. The last state of the process should satisfy one of the goal states.
    last_state = process_states[max_workflow_trace_count - 1]
    model.add(state_satisfies_requirements_set(last_state, m_st))

    

    def last_index_constraint(i):
        trace = workflow_trace[i]
        # if trace == 0:
        #   Conjunction([workflow_trace[j] == 0 for j in range(i + 1, max_workflow_trace_count)])  
        return (trace != 0) | Conjunction(
            [workflow_trace[j] == 0 for j in range(i + 1, max_workflow_trace_count)])
        
    # model.add([last_index_constraint(i)
    #            for i in range(0, max_workflow_trace_count - 1)])

    return (
        model,
        workflow_trace,
        process_states,
        last_task_index
    )
