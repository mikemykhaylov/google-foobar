class Graph:
    def __init__(self):
        legal_moves = {}
        for i in range(0, 64):
            cell_legal_moves = []

            if i >= 17 and i % 8 != 0:
                cell_legal_moves.append(-17)
            if i >= 15 and i % 8 != 7:
                cell_legal_moves.append(-15)
            if i >= 10 and i % 8 >= 2:
                cell_legal_moves.append(-10)
            if i >= 6 and i % 8 < 6:
                cell_legal_moves.append(-6)
            if i <= 55 and i % 8 >= 2:
                cell_legal_moves.append(6)
            if i <= 53 and i % 8 <= 5:
                cell_legal_moves.append(10)
            if i <= 47 and i % 8 != 0:
                cell_legal_moves.append(15)
            if i <= 46 and i % 8 != 7:
                cell_legal_moves.append(17)

            cell_legal_moves = [str(x + i) for x in cell_legal_moves]
            legal_moves[str(i)] = cell_legal_moves
        self.adjacency_list = legal_moves

    def find_paths(self, vert, vert2):
        vert = str(vert)
        vert2 = str(vert2)
        queue = []
        distances = {}

        queue.insert(0, {"vert": vert, "distance": 0})

        while len(queue) > 0:
            currentVert = queue.pop()
            currentVertName = currentVert["vert"]
            currentVertDist = currentVert["distance"]

            if currentVertName in distances:
                continue
            else:
                distances[currentVertName] = currentVertDist
            for neighbour in self.adjacency_list[currentVertName]:
                if neighbour not in distances:
                    queue.insert(
                        0, {"vert": neighbour, "distance": currentVertDist + 1}
                    )

        return distances[vert2]


chess = Graph()
for key in chess.adjacency_list:
    print(key, chess.adjacency_list[key])
# print(chess.find_paths(0,1))
