from Numberjack import *

max_executions = 2
tasks_count = 3
data_entities_count = 4

max_workflow_trace_count = tasks_count * max_executions

workflow_trace = VarArray(max_workflow_trace_count, 1, tasks_count, 'task')

process_states = Matrix(max_workflow_trace_count, data_entities_count, -1, 2)

model = Model()

# No more than max_execution occurances of task in workflow trace
model.add([Cardinality(workflow_trace, x) <= max_executions for x in range(1, tasks_count + 1)])


solver = model.load('MiniSat')

solver.startNewSearch()

while solver.getNextSolution() == SAT:
    print([x.get_value() for x in workflow_trace])
