import math

class GraphReader:
    """
    Read the graph from a txt file.
    The file should be in the format city, x, y.
    """
    def __init__(self, filename):
        self.__cities = []
        self.__points = []
        with open(filename, 'r') as file:
            for line in file.readlines():
                city = line.split(' ')
                self.__cities.append(dict(index=int(city[0]), x=float(city[1]), y=float(city[2])))
                self.__points.append((float(city[1]), float(city[2])))

        self.__cost_matrix = []
        rank = len(self.__cities)
        for i in range(rank):
            row = []
            for j in range(rank):
                row.append(self.distance(self.__cities[i], self.__cities[j]))
            self.__cost_matrix.append(row)
    
    def get_graph(self):
        return self.__cost_matrix

    def get_cities(self):
        return self.__cities

    @staticmethod
    def distance(city1: dict, city2: dict):
        return math.sqrt((city1['x'] - city2['x'])**2 + (city1['y'] - city2['y'])**2)