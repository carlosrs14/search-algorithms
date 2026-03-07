import math
import heapq

class GraphReader:
    """
    Read the graph from a txt file.
    The file should be in the format index x y.
    Convert coordinates to normalized 0-1 range and build a K-nearest-neighbor graph.
    """
    def __init__(self, filename, k_neighbors=4):
        self.__cities = []
        raw_cities = []
        
        # Read file
        import sys
        try:
            with open(filename, 'r') as file:
                for line in file.readlines():
                    if not line.strip():
                        continue
                    city = line.strip().split(' ')
                    raw_cities.append({'index': int(city[0]), 'x': float(city[1]), 'y': float(city[2])})
        except Exception as e:
            print(f"Error reading {filename}: {e}", file=sys.stderr)

        # Normalize coordinates between 0.05 and 0.95 (to leave some padding)
        if raw_cities:
            min_x = min(city['x'] for city in raw_cities)
            max_x = max(city['x'] for city in raw_cities)
            min_y = min(city['y'] for city in raw_cities)
            max_y = max(city['y'] for city in raw_cities)
            
            range_x = max_x - min_x if max_x > min_x else 1
            range_y = max_y - min_y if max_y > min_y else 1
            
            for city in raw_cities:
                norm_x = 0.05 + 0.9 * ((city['x'] - min_x) / range_x)
                norm_y = 0.05 + 0.9 * ((city['y'] - min_y) / range_y)
                self.__cities.append({'index': city['index'] - 1, 'x': norm_x, 'y': norm_y})
        
        # Calculate distances and build K-NN graph
        self.__cost_matrix = []
        rank = len(self.__cities)
        
        # Initialize empty adj matrix
        self.__cost_matrix = [[0.0 for _ in range(rank)] for _ in range(rank)]
        
        for i in range(rank):
            distances = []
            for j in range(rank):
                if i != j:
                    dist = self.distance(self.__cities[i], self.__cities[j])
                    distances.append((dist, j))
            
            # Keep only k-nearest neighbors
            distances.sort()
            for k in range(min(k_neighbors, len(distances))):
                dist, j = distances[k]
                self.__cost_matrix[i][j] = dist
                self.__cost_matrix[j][i] = dist # Make it undirected

    def get_graph(self):
        return self.__cost_matrix

    def get_cities(self):
        return self.__cities

    @staticmethod
    def distance(city1: dict, city2: dict):
        return math.sqrt((city1['x'] - city2['x'])**2 + (city1['y'] - city2['y'])**2)