from itertools import permutations
from copy import deepcopy


class Graph:
    def __init__(self, adjacency_matrix=[]):
        self.adjacency_matrix = adjacency_matrix
        self.node_count = len(adjacency_matrix)

    def add_vertex(self, adjacency_matrix=[]):
        if adjacency_matrix == None:
            adjacency_matrix = self.adjacency_matrix
        adjacency_matrix.append([None])
        for i in range(len(adjacency_matrix) - 1):
            adjacency_matrix[i].append(None)
            adjacency_matrix[len(adjacency_matrix) - 1].append(None)
        return len(adjacency_matrix) - 1

    def add_egde(self, vertex1, vertex2, weight, adjacency_matrix=[]):
        if adjacency_matrix == None:
            adjacency_matrix = self.adjacency_matrix
        adjacency_matrix[vertex1][vertex2] = weight

    def floyd_warshall_apsp(self):
        # Memoized smallest paths
        # If memo[i][j] = 3 then the smallest current path between i and j is 3
        memo = deepcopy(self.adjacency_matrix)

        # Floyd-Warshall algorithm body, gives best distance between all pairs of nodes
        for i in range(self.node_count):
            for j in range(self.node_count):
                for k in range(self.node_count):
                    if memo[i][k] + memo[k][j] < memo[i][j]:
                        memo[i][j] = memo[i][k] + memo[k][j]

        # If a path to itself is less than 0 for some node, there's a negative loop
        has_negative_loop = False
        for i in range(self.node_count):
            if memo[i][i] < 0:
                has_negative_loop = True
            if has_negative_loop:
                break

        return [memo, has_negative_loop]

    def max_visits(self, time_limit):
        floyd_warshall_output = self.floyd_warshall_apsp()
        shortest_paths_matrix = floyd_warshall_output[0]
        has_negative_loop = floyd_warshall_output[1]
        bunny_numbers = [i for i in range(1, self.node_count - 1)]

        if has_negative_loop:
            return [x - 1 for x in bunny_numbers]

        possible_bunny_orders = []
        for i in range(self.node_count - 2, 0, -1):
            # print(f'Making permutations of length {i}')
            orders_of_bunny_visiting = list(permutations(bunny_numbers, i))
            for order in orders_of_bunny_visiting:
                # print(f'Working with order 0 -> {order} -> 4')
                total = time_limit
                # print(f"Distance from 0 to {order[0]} = {shortest_paths_matrix[0][order[0]]}")
                total -= shortest_paths_matrix[0][order[0]]
                if i >= 2:
                    # print("Permutation longer than 1, have to consider inside connections")
                    for j in range(i - 1):
                        # print(f"Distance from {order[j]} to {order[j+1]} = {shortest_paths_matrix[0][order[0]]}")
                        total -= shortest_paths_matrix[order[j]][order[j + 1]]
                # print(f"Distance from {order[i-1]} to {self.node_count - 1} = {shortest_paths_matrix[order[i - 1]][self.node_count - 1]}")
                total -= shortest_paths_matrix[order[i - 1]][self.node_count - 1]
                if total >= 0:
                    # print(f'Total is {total}. Order 0 -> {order} -> 4 can be made in time!')
                    possible_bunny_orders.append(order)
                # print('\n')

        # print(possible_bunny_orders)
        max_bunny_order_length = max([len(x) for x in possible_bunny_orders])
        max_length_bunny_orders = [
            order
            for order in possible_bunny_orders
            if len(order) == max_bunny_order_length
        ]
        min_bunny_order_ids_sum = min([sum(order) for order in max_length_bunny_orders])
        max_length_min_ids_bunny_orders = [
            order
            for order in max_length_bunny_orders
            if sum(order) == min_bunny_order_ids_sum
        ]
        output = list(max_length_min_ids_bunny_orders[0])
        output.sort()
        return [x - 1 for x in output]


def solution(times, time_limit):
    graph = Graph(times)
    return graph.max_visits(time_limit)


tms1 = [
    [0, 2, 2, 2, -1],
    [9, 0, 2, 2, -1],
    [9, 3, 0, 2, -1],
    [9, 3, 2, 0, -1],
    [9, 3, 2, 2, 0],
]
lim1 = 1

tms2 = [
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 0],
]
lim2 = 3

solution(tms1, lim1)
