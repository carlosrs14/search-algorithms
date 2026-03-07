import pygame
from utils.colors import BACKGROUND, NODE_COLOR, EDGE_COLOR, START_COLOR, END_COLOR, VISITED_COLOR, FRONTIER_COLOR, PATH_COLOR

class Map:
    def __init__(self, cities, width, height, padding=50):
        self.cities = cities
        self.width = width
        self.height = height
        self.padding = padding

        # Since we normalized between 0-1, we can just use the width and height
        self.scale_x = (self.width - 2 * self.padding)
        self.scale_y = (self.height - 2 * self.padding)

    def _scale_point(self, city):
        x = city['x'] * self.scale_x + self.padding
        y = city['y'] * self.scale_y + self.padding
        return int(x), int(y)

    def get_city_at_pos(self, pos, radius=15):
        for i, city in enumerate(self.cities):
            cx, cy = self._scale_point(city)
            if (pos[0] - cx)**2 + (pos[1] - cy)**2 <= radius**2:
                return i
        return None

    def draw(self, screen, graph, frontier, visited, current_node, path, start_node, end_node):
        screen.fill(BACKGROUND)
        
        # Draw all edges first (faint)
        rank = len(self.cities)
        for i in range(rank):
            for j in range(i + 1, rank):
                if graph[i][j] > 0:
                    start_pos = self._scale_point(self.cities[i])
                    end_pos = self._scale_point(self.cities[j])
                    pygame.draw.line(screen, EDGE_COLOR, start_pos, end_pos, 1)

        # Draw path if available
        if path:
            if len(path) > 1:
                path_points = [self._scale_point(self.cities[i]) for i in path]
                pygame.draw.lines(screen, PATH_COLOR, False, path_points, 4)
        
        # Draw cities
        for i, city in enumerate(self.cities):
            pos = self._scale_point(city)
            color = NODE_COLOR
            radius = 4
            
            if i in visited:
                color = VISITED_COLOR
                radius = 5
            
            if i in frontier:
                color = FRONTIER_COLOR
                radius = 6

            if i == current_node:
                color = (255, 255, 255)
                radius = 8
            
            if i == start_node:
                color = START_COLOR
                radius = 8
            elif i == end_node:
                color = END_COLOR
                radius = 8
            
            pygame.draw.circle(screen, color, pos, radius)
