import json
from sys import getsizeof


class Graph:
    def __init__(self, adjacency_matrix=[], sources=[], sinks=[]):
        self.adjacency_matrix = [
            [_el if _el != 0 else None for _el in _ar] for _ar in adjacency_matrix
        ]

        # "Entrances and exits are disjoint"
        for i in sinks:
            for j in sources:
                self.adjacency_matrix[i][j] = None

        # Setting corridors in both sides
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] is not None:
                    self.adjacency_matrix[j][i] = self.adjacency_matrix[i][j]

        # Capacity scaling optimization
        max_capacity_value = max(map(max, adjacency_matrix))
        self.delta = 1
        for i in range(8 * getsizeof(max_capacity_value)):
            curr = 1 << i
            if curr > max_capacity_value:
                break
            self.delta = curr
        self.max_delta = self.delta

    def add_vertex(self):
        # Adding new vertex to a graph
        self.adjacency_matrix.append([None])
        for i in range(len(self.adjacency_matrix) - 1):
            self.adjacency_matrix[i].append(None)
            self.adjacency_matrix[len(self.adjacency_matrix) - 1].append(None)
        # Length - 1 is the vertex itself
        return len(self.adjacency_matrix) - 1

    def add_egde(self, vertex1, vertex2, weight):
        self.adjacency_matrix[vertex1][vertex2] = weight
        self.adjacency_matrix[vertex2][vertex1] = weight

    def mathematica_print(self, adjMatrix=None):
        if adjMatrix == None:
            adjMatrix = self.adjacency_matrix
        return (
            json.dumps(adjMatrix)
            .replace("null", "0")
            .replace("[", "{")
            .replace("]", "}")
        )

    def pretty_print(self):
        s = [[str(e) for e in row] for row in self.adjacency_matrix]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "\t".join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print("\n\n".join(table))

    def __get_vertex_neighbours(self, vert, adjMatrix=None):
        if adjMatrix == None:
            adjMatrix = self.adjacency_matrix
        output = []
        for i in range(len(adjMatrix[vert])):
            if adjMatrix[vert][i] is not None:
                output.append(i)
        return output

    def __get_recursive__path(self, vert, prev):
        if prev[vert] == None:
            return [vert]
        return [vert, *self.__get_recursive__path(prev[vert], prev)]

    def bfs(self, vert):
        queue = []
        visited = {}

        queue.append({"vert": vert, "dist": 0})

        while len(queue) != 0:
            current_vert_dict = queue.pop(0)
            current_vert = current_vert_dict["vert"]
            current_vert_dist = current_vert_dict["dist"]
            if current_vert in visited.keys():
                continue
            else:
                visited[current_vert] = current_vert_dist

            vert_neighbours = self.__get_vertex_neighbours(current_vert)

            # print(f"Neighbours of {current_vert} are {vert_neighbours}")

            for neighbour in vert_neighbours:
                if (
                    neighbour not in visited.keys()
                    and self.adjacency_matrix[current_vert][neighbour] > 0
                ):
                    queue.append({"vert": neighbour, "dist": current_vert_dist + 1})
        return visited

    def __get_level_graph(self, distances):
        level_graph = []
        for i in range(len(self.adjacency_matrix)):
            level_graph.append([])
            for j in range(len(self.adjacency_matrix)):
                if (
                    self.adjacency_matrix[i][j] is None
                    or self.adjacency_matrix[i][j] == 0
                    or distances[j] - distances[i] != 1
                ):
                    level_graph[i].append(None)
                    continue
                else:
                    level_graph[i].append(self.adjacency_matrix[i][j])

        return level_graph

    def dfs(self, vert1, vert2=None, delta=0, adjMatrix=None):
        if adjMatrix == None:
            adjMatrix = self.adjacency_matrix
        prev = {}
        visited = []

        prev[vert1] = None

        def dfs_recursive(vert):
            # print(f"Working with {vert}")
            # print(f"Visited: {visited}\n")
            result = [vert]
            visited.append(vert)
            vert_neighbours = self.__get_vertex_neighbours(vert, adjMatrix)
            # print(f"Neighbours: {vert_neighbours}\n")

            unvisited_vert_neighbours = [
                elem for elem in vert_neighbours if elem not in visited
            ]

            min_flow_val = max(delta, 1)

            if len(unvisited_vert_neighbours) == 0 or (
                vert2 is not None and vert2 in visited
            ):
                return result

            for neighbour in unvisited_vert_neighbours:
                if adjMatrix[vert][neighbour] >= min_flow_val:
                    prev[neighbour] = vert
                    result = [*result, *dfs_recursive(neighbour)]
            return result

        traversed_path = dfs_recursive(vert1)

        if vert2 is not None:
            if vert2 not in prev:
                output = []
            else:
                output = self.__get_recursive__path(vert2, prev)
                output.reverse()
        else:
            output = traversed_path
        # output = list(map(lambda x: x + 1, output))
        return output

    def augment_path(self, path, adjMatrix=None):
        # This method is used both in Ford-Fulkerson and in Dinic's
        # If the former is the case, the only place where flow must be augmented is self.adjacency_matrix
        # Therefore, we dont project changes in flow to any other place
        # If, however, we call this from Dinic's algorithm method, we pass in the level graph
        # In that case we augment flow in two places:
        # 1. In the level graph (without residual edges), so that not to create new edges for DFS
        # 2. In self.adjacency_matrix (with residual edges), so that BFS distances evolve as we augment flow
        # project_changes defines whether we put changes only in self.adjacency_matrix, or in the passed matrix as well

        project_changes = True
        if adjMatrix == None:
            adjMatrix = self.adjacency_matrix
            project_changes = False

        edges = []
        for i in range(len(path) - 1):
            edges.append([path[i], path[i + 1], adjMatrix[path[i]][path[i + 1]]])
        print(f"Path's capacities are: {list(map(lambda edge: edge[2], edges))}")
        max_path_flow = min(*list(map(lambda edge: abs(edge[2]), edges)))
        for edge in edges:
            # If project_changes, we augment the flow in the passed matrix also
            self.adjacency_matrix[edge[0]][edge[1]] -= max_path_flow
            if project_changes:
                adjMatrix[edge[0]][edge[1]] -= max_path_flow
        return max_path_flow

    def ford_fulkerson_max_flow(self, source, sink):
        total = 0
        while True:
            path = self.dfs(source, sink, self.delta)
            if len(path) == 0:
                print(f"No path found for delta {self.delta}")
                if self.delta > 1:
                    self.delta /= 2
                    print("\n")
                    continue
                else:
                    break
            else:
                print(f"Path {list(map(lambda x: x + 1, path))} found!")
                path_max_flow = self.augment_path(path)
                print(f"Path's max flow is {path_max_flow}")
                total += path_max_flow
            print("\n")
        return total

    def dinics_max_flow(self, source, sink):
        total = 0

        while True:
            # Find distances to each point on the graph
            distances = self.bfs(source)
            if sink not in distances:
                print("No path found during BFS phase, returning")
                break
            # Construct the level graph for Dinic's
            level_graph = self.__get_level_graph(distances)
            while True:
                # Find some path with DFS and capacity scaling
                path = self.dfs(source, sink, self.delta, level_graph)
                if len(path) == 0:
                    print(f"No path found for delta {self.delta}")
                    if self.delta > 1:
                        self.delta /= 2
                        print("\n")
                        continue
                    else:
                        self.delta = self.max_delta
                        break
                else:
                    print(f"Path {list(map(lambda x: x + 1, path))} found!")
                    path_max_flow = self.augment_path(path, level_graph)
                    print(f"Path's max flow is {path_max_flow}")
                    total += path_max_flow
                print("\n")
        return total


def solution(sources, sinks, adjMatrix):
    max_possible_flow = 2000000

    graph = Graph(adjMatrix, sources, sinks)

    root_source = graph.add_vertex()
    for source in sources:
        graph.add_egde(root_source, source, max_possible_flow)

    root_sink = graph.add_vertex()
    for sink in sinks:
        graph.add_egde(sink, root_sink, max_possible_flow)

    return graph.dinics_max_flow(root_source, root_sink)
