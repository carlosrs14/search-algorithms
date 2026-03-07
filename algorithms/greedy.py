from algorithms import algorithm
from utils.reader import GraphReader
import heapq

class Greedy(algorithm.Algorithm):
    def __init__(self, graph, start_node, end_node, cities):
        super().__init__(graph, start_node, end_node)
        self.cities = cities
        self.came_from = {start_node: None}
        self.pq = [(self._heuristic(start_node, end_node), start_node)]
        self.closed_set = set()

    def _heuristic(self, node1, node2):
        return GraphReader.distance(self.cities[node1], self.cities[node2])

    def solve(self):
        self.frontier.add(self.start_node)
        yield self.frontier, self.closed_set, self.start_node, [self.start_node]

        while self.pq:
            _, current_node = heapq.heappop(self.pq)
            self.frontier.discard(current_node)
            
            if current_node in self.closed_set:
                continue

            self.closed_set.add(current_node)

            if current_node == self.end_node:
                yield self.frontier, self.closed_set, current_node, self.reconstruct_path()
                return

            for neighbor in range(len(self.graph[current_node])):
                if self.graph[current_node][neighbor] > 0: # Connected
                    if neighbor not in self.closed_set:
                        self.came_from[neighbor] = current_node
                        heapq.heappush(self.pq, (self._heuristic(neighbor, self.end_node), neighbor))
                        self.frontier.add(neighbor)
            
            yield self.frontier, self.closed_set, current_node, self.reconstruct_path(current_node)

    def reconstruct_path(self, target_node=None):
        if target_node is None:
            target_node = self.end_node
        path = []
        current_node = target_node
        while current_node is not None:
            path.append(current_node)
            if current_node == self.start_node:
                break
            current_node = self.came_from.get(current_node)
        path.reverse()
        return path
