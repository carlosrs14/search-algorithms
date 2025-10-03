import pygame
from utils.colors import BLACK, WHITE, BLUE, RED, GREEN


class Map:
    def __init__(self, cities, width, height, padding=50):
        self.cities = cities
        self.width = width
        self.height = height
        self.padding = padding

        # Find the bounding box of the cities
        min_x = min(city['x'] for city in cities)
        max_x = max(city['x'] for city in cities)
        min_y = min(city['y'] for city in cities)
        max_y = max(city['y'] for city in cities)

        # Calculate scaling factors
        self.scale_x = (self.width - 2 * self.padding) / (max_x - min_x)
        self.scale_y = (self.height - 2 * self.padding) / (max_y - min_y)

        self.offset_x = self.padding - min_x * self.scale_x
        self.offset_y = self.padding - min_y * self.scale_y

    def _scale_point(self, city):
        x = city['x'] * self.scale_x + self.offset_x
        y = city['y'] * self.scale_y + self.offset_y
        return int(x), int(y)

    def draw(self, screen, path=None, start_node=None, end_node=None):
        # Draw path if available
        if path:
            path_points = [self._scale_point(self.cities[i]) for i in path]
            pygame.draw.lines(screen, BLUE, False, path_points, 5)

        # Draw cities
        for i, city in enumerate(self.cities):
            pos = self._scale_point(city)
            color = BLACK
            if i == start_node:
                color = GREEN # Start node
            elif i == end_node:
                color = RED   # End node
            
            pygame.draw.circle(screen, color, pos, 5)
