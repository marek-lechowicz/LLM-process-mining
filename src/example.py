from Numberjack import *

max_executions = 4
tasks_count = 5

workflow_trace = VarArray(tasks_count * max_executions)

x = Variable(7)

model = Model(x > 3)

solver = model.load('MiniSat')

solver.startNewSearch()

while solver.getNextSolution() == SAT:
    print(x)
