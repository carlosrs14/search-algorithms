from abc import abstractmethod

class Algorithm:
    
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start_node = start
        self.end_node = end
        self.path = []
        self.visited = []

    @abstractmethod
    def solve(self):
        raise NotImplementedError

    @abstractmethod
    def reconstruct_path(self):
        raise NotImplementedError
