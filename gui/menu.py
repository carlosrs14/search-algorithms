import pygame
from utils.colors import BLACK, WHITE, BLUE

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 40)
        self.title_font = pygame.font.Font(None, 60)

        self.algorithms = ['BFS', 'DFS', 'A*']
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        button_width = 200
        button_height = 50
        x = (self.screen_width - button_width) / 2
        y_start = 150
        y_gap = 70

        for i, algo in enumerate(self.algorithms):
            y = y_start + i * y_gap
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append({'rect': rect, 'text': algo, 'algo': algo})

    def draw(self, screen):
        # Draw title
        title_surface = self.title_font.render("Select an Algorithm", True, BLACK)
        title_rect = title_surface.get_rect(center=(self.screen_width / 2, 80))
        screen.blit(title_surface, title_rect)

        # Draw buttons
        for button in self.buttons:
            pygame.draw.rect(screen, BLUE, button['rect'])
            text_surface = self.font.render(button['text'], True, WHITE)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        return button['algo']
        return None
