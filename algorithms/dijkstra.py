from algorithms import algorithm
import heapq

class Dijkstra(algorithm.Algorithm):
    def __init__(self, graph, start_node, end_node):
        super().__init__(graph, start_node, end_node)
        self.distances = {i: float('inf') for i in range(len(graph))}
        self.distances[start_node] = 0
        self.came_from = {start_node: None}
        self.pq = [(0, start_node)]
        self.closed_set = set()

    def solve(self):
        self.frontier.add(self.start_node)
        yield self.frontier, self.closed_set, self.start_node, [self.start_node]

        while self.pq:
            current_distance, current_node = heapq.heappop(self.pq)
            self.frontier.discard(current_node)

            if current_node in self.closed_set:
                continue
                
            self.closed_set.add(current_node)

            if current_node == self.end_node:
                yield self.frontier, self.closed_set, current_node, self.reconstruct_path()
                return

            for neighbor in range(len(self.graph[current_node])):
                if self.graph[current_node][neighbor] > 0: # Connected
                    weight = self.graph[current_node][neighbor]
                    distance = current_distance + weight

                    if distance < self.distances[neighbor]:
                        self.distances[neighbor] = distance
                        self.came_from[neighbor] = current_node
                        heapq.heappush(self.pq, (distance, neighbor))
                        self.frontier.add(neighbor)
            
            yield self.frontier, self.closed_set, current_node, self.reconstruct_path(current_node)

    def reconstruct_path(self, target_node=None):
        if target_node is None:
            target_node = self.end_node
        path = []
        current_node = target_node
        while current_node is not None:
            path.append(current_node)
            current_node = self.came_from.get(current_node)
        path.reverse()
        return path
