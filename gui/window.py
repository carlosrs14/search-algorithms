import pygame
import sys

class Window:
    def __init__(self, sizes, title):
        pygame.init()
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
    
    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.update()
            pygame.display.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def get_screen(self):
        return self.screen

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_clock(self):
        return self.clock

    def update(self):
        pygame.display.update()
