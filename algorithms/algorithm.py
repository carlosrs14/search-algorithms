from abc import abstractmethod

class Algorithm:
    
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start_node = start
        self.end_node = end
        self.path = []
        self.visited = set()
        self.frontier = set()

    @abstractmethod
    def solve(self):
        """
        Generator that returns the state of the algorithm at each step explicitly.
        Yields: (frontier_set, visited_set, current_node, current_path)
        """
        raise NotImplementedError

    @abstractmethod
    def reconstruct_path(self):
        raise NotImplementedError
