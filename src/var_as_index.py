from Numberjack import *


array = VarArray(5, 6)

m = [
    [0, 1, 2, 3, 4],
    [1, 2, 3, 4, 5],
    [2, 3, 4, 5, 6],
    [3, 4, 5, 6, 7],
    [4, 5, 6, 7, 8],
    [5, 6, 7, 8, 9]
]
matrix = Matrix(5, 6, 10)

def matrixElements(matrix_var, matrix):
    constraints = []
    for i in range(0, 5):
        for j in range(0, 5):
            constraints.append(matrix_var[i][j] == matrix[i][j])
    return constraints

idx = Variable(5)


model = Model()

model.add(matrixElements(matrix, m))
model.add([matrix[idx, i] == array[i] for i in range(0, 5)])



solver = model.load('MiniSat')
solver.startNewSearch()


while solver.getNextSolution() == SAT:
    print(idx, array)
