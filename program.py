# import json
# from geometry.matrix_reading import Task
# from Alg_Little.Alg_L_Classes import algorithm_Lit
# def main():
#     with open('geometry/data4.json') as file:
#         dt = json.load(file)

#     t = Task(dt)
#     matrix = t.length_matrix
#     s = t.length_matrix.shape[0]
#     ans, answer = algorithm_Lit(matrix, s, 4)
#     print(ans, answer)

# if __name__ == '__main__':
#     main()
def has_cycle(edges: list[tuple]):
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    rec_stack = set()
    cycle_nodes = set()  # Для хранения вершин цикла

    def dfs(node):
        if node in rec_stack:
            cycle_nodes.add(node)  # Добавляем вершину в цикл
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in graph:
                return False
            if dfs(neighbor):
                cycle_nodes.add(node)  # Добавляем вершину в цикл
                return True

        rec_stack.remove(node)
        return False

    for vertex in graph:
        if dfs(vertex):
            return True, len(cycle_nodes)  # Возвращаем True и количество вершин в цикле
    return False, 0  # Если цикла нет, возвращаем False и 0

# Пример использования
edges = [(1, 2), (2, 3), (3, 4), (6, 5), (5, 1), (4, 6)]
has_cycle_result, cycle_count = has_cycle(edges)
print(f"Цикл найден: {has_cycle_result}, количество вершин в цикле: {cycle_count}")