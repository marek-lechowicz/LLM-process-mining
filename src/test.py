from Numberjack import *

m_tc = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

m = VarArray(3 * 2, 0, 3)

x = [1, 2, 3]

def constraint(i):
    t == m[i]
    effects = VarArray(3)
    effects_constraints = [effects[x] == m_tc[t, x] for x in range(0, 3)]

model = Model()

model.add([constraint(i) for i in range(0, 6)])


solver = model.load('MiniSat')
solver.startNewSearch()

while solver.getNextSolution() == SAT:
    print(m)



