from Numberjack import *

def test(constraint):
    x = Variable('x')
    y = Variable('y')

    model = Model()
    constr = constraint(x, y)
    # model.add(constr)
    model.add((x == 0 ) == (y == 1))

    print(constr)
    print(model)

    solver = model.load('Mistral')
    solver.startNewSearch()
    solutions = 0
    while solver.getNextSolution() == SAT:
        print(f'x = {x}, y = {y}')
        solutions += 1
    print(f'Solutions: {solutions}')
    print()


test(lambda x, y: x == y)
test(lambda x, y: x != y)
test(lambda x, y: Ne([x, y]))
test(lambda x, y: Neg(x))
test(lambda x, y: -(x == y))
