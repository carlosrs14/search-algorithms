from algorithms import algorithm
from collections import deque

class BFS(algorithm.Algorithm):
    def __init__(self, graph, start_node, end_node):
        super().__init__(graph, start_node, end_node)
        self.queue = deque([self.start_node])
        self.visited = {self.start_node}
        self.came_from = {self.start_node: None}

    def solve(self):
        while self.queue:
            current_node = self.queue.popleft()

            if current_node == self.end_node:
                return self.reconstruct_path()

            for neighbor in range(len(self.graph[current_node])):
                if self.graph[current_node][neighbor] > 0 and neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.came_from[neighbor] = current_node
                    self.queue.append(neighbor)
        
        return None

    def reconstruct_path(self):
        path = []
        current_node = self.end_node
        while current_node is not None:
            path.append(current_node)
            current_node = self.came_from[current_node]
        path.reverse()
        return path
