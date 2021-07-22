from random import choice
from string import ascii_letters

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if not vertex in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_egde(self, vertex1, vertex2):
        self.adjacency_list[vertex1].append(vertex2)

    def paths_of_len_from_vert(self, vertex):
        number = 0
        if len(self.adjacency_list[vertex]) == 0:
            return 0
        for neighbour in self.adjacency_list[vertex]:
            # print(neighbour)
            if len(self.adjacency_list[neighbour]) == 0:
                continue
            number += len(self.adjacency_list[neighbour])

        return number

def encode(num):
  stringified = str(num)
  return stringified + (''.join(choice(ascii_letters) for i in range(10)))


def solution(passed_list):
    coded_list = list(map(encode, passed_list))
    graph = Graph()
    for i in range(len(coded_list)):
        graph.add_vertex(coded_list[i])
        for j in range(i + 1, len(coded_list)):
            numerator = int(coded_list[j][:len(coded_list[j]) - 10])
            denominator = int(coded_list[i][:len(coded_list[i]) - 10])
            if numerator % denominator == 0:
                graph.add_egde(coded_list[i], coded_list[j])

    output = 0
    for i in graph.adjacency_list.keys():
        output += graph.paths_of_len_from_vert(i)
    return output


print(solution([1,1,1]))