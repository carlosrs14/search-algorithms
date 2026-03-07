import heapq
from algorithms import algorithm
from utils.reader import GraphReader

class AStar(algorithm.Algorithm):
    def __init__(self, graph, start_node, end_node, cities):
        super().__init__(graph, start_node, end_node)
        self.cities = cities
        
        self.closed_set = set()

        self.open_set = [(self._heuristic(start_node, end_node), start_node)]
        
        self.came_from = {}

        self.g_score = {i: float('inf') for i in range(len(graph))}
        self.g_score[start_node] = 0

        self.f_score = {i: float('inf') for i in range(len(graph))}
        self.f_score[start_node] = self._heuristic(start_node, end_node)

    def _heuristic(self, node1, node2):
        return GraphReader.distance(self.cities[node1], self.cities[node2])

    def solve(self):
        self.frontier.add(self.start_node)
        yield self.frontier, self.closed_set, self.start_node, [self.start_node]

        while self.open_set:
            _, current_node = heapq.heappop(self.open_set)
            self.frontier.discard(current_node)

            if current_node == self.end_node:
                yield self.frontier, self.closed_set, current_node, self.reconstruct_path()
                return

            self.closed_set.add(current_node)

            for neighbor in range(len(self.graph[current_node])):
                if self.graph[current_node][neighbor] > 0: # If there is a connection
                    if neighbor in self.closed_set:
                        continue

                    tentative_g_score = self.g_score[current_node] + self.graph[current_node][neighbor]

                    if tentative_g_score < self.g_score[neighbor]:
                        self.came_from[neighbor] = current_node
                        self.g_score[neighbor] = tentative_g_score
                        self.f_score[neighbor] = tentative_g_score + self._heuristic(neighbor, self.end_node)
                        
                        in_open_set = False
                        for _, n in self.open_set:
                            if n == neighbor:
                                in_open_set = True
                                break
                        if not in_open_set:
                            heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor))
                            self.frontier.add(neighbor)
            
            yield self.frontier, self.closed_set, current_node, self.reconstruct_path(current_node)

    def reconstruct_path(self, target_node=None):
        if target_node is None:
            target_node = self.end_node
        path = []
        current_node = target_node
        while current_node in self.came_from:
            path.append(current_node)
            current_node = self.came_from[current_node]
        path.append(self.start_node)
        path.reverse()
        return path
