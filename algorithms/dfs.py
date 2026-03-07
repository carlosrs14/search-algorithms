from algorithms import algorithm

class DFS(algorithm.Algorithm):
    def __init__(self, graph, start_node, end_node):
        super().__init__(graph, start_node, end_node)
        self.stack = [self.start_node]
        self.visited = {self.start_node}
        self.came_from = {self.start_node: None}
    
    def solve(self):
        self.frontier.add(self.start_node)
        yield self.frontier, self.visited, self.start_node, [self.start_node]

        while self.stack:
            current_node = self.stack.pop()
            self.frontier.discard(current_node)
            self.visited.add(current_node)

            if current_node == self.end_node:
                yield self.frontier, self.visited, current_node, self.reconstruct_path()
                return
            
            for neighbor in range(len(self.graph[current_node])):
                if self.graph[current_node][neighbor] > 0 and neighbor not in self.visited and neighbor not in self.frontier:
                    self.frontier.add(neighbor)
                    self.came_from[neighbor] = current_node
                    self.stack.append(neighbor)
        
            yield self.frontier, self.visited, current_node, self.reconstruct_path(current_node)

    def reconstruct_path(self, target_node=None):
        if target_node is None:
            target_node = self.end_node
        path = []
        current_node = target_node
        while current_node is not None:
            path.append(current_node)
            current_node = self.came_from[current_node]
        path.reverse()
        return path