import json
from geometry.matrix_reading import Task
from Alg_Little.Alg_L_Classes import algorithm_Lit
def main():
    with open('geometry/data4.json') as file:
        dt = json.load(file)

    t = Task(dt)
    matrix = t.length_matrix
    s = t.length_matrix.shape[0]
    ans, answer = algorithm_Lit(matrix, s, 4)
    print(ans, answer)

if __name__ == '__main__':
    main()