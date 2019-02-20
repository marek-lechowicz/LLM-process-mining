def matrixElements(matrix_var, matrix):
    assert len(matrix) == len(matrix_var)
    assert len(matrix) > 0
    assert len(matrix[0]) == len(matrix_var[0])

    constraints = []

    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[0])):
            constraints.append(matrix_var[i][j] == matrix[i][j])
    return constraints

def varArrayElements(var_array, list):
    assert len(var_array) == len(list)
    return [var_array[i] == list[i] for i in range(0, len(list))]

def VarArray_to_list(var_array):
    return [x.get_value() for x in var_array]

def Matrix_to_list(matrix):
    return [VarArray_to_list(row) for row in matrix]
