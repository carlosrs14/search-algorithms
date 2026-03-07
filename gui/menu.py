import pygame
from utils.colors import PANEL_BG, BUTTON_BG, BUTTON_HOVER, BUTTON_ACTIVE, TEXT_COLOR

class Menu:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.title_font = pygame.font.SysFont("Segoe UI", 32, bold=True)
        self.instructions_font = pygame.font.SysFont("Segoe UI", 16)

        self.algorithms = ['BFS', 'DFS', 'A*', 'Dijkstra', 'Greedy']
        self.buttons = []
        self.active_algo = None
        
        self.hovered_algo = None
        self._create_buttons()

    def _create_buttons(self):
        button_width = self.rect.width - 40
        button_height = 45
        x = self.rect.x + 20
        y_start = self.rect.y + 100
        y_gap = 60

        for i, algo in enumerate(self.algorithms):
            y = y_start + i * y_gap
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append({'rect': rect, 'text': algo, 'algo': algo})

    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, PANEL_BG, self.rect)
        pygame.draw.line(screen, (50, 50, 60), (self.rect.x, 0), (self.rect.x, self.rect.height), 2)

        # Draw title
        title_surface = self.title_font.render("Algorithms", True, TEXT_COLOR)
        screen.blit(title_surface, (self.rect.x + 20, self.rect.y + 30))

        # Instructions
        inst_surf1 = self.instructions_font.render("Left Click Node: Set Start", True, (150, 150, 160))
        inst_surf2 = self.instructions_font.render("Right Click Node: Set End", True, (150, 150, 160))
        inst_surf3 = self.instructions_font.render("Space: Play/Pause", True, (150, 150, 160))
        
        dy = self.rect.height - 100
        screen.blit(inst_surf1, (self.rect.x + 20, dy))
        screen.blit(inst_surf2, (self.rect.x + 20, dy + 25))
        screen.blit(inst_surf3, (self.rect.x + 20, dy + 50))


        # Draw buttons
        for button in self.buttons:
            color = BUTTON_BG
            if button['algo'] == self.active_algo:
                color = BUTTON_ACTIVE
            elif button['algo'] == self.hovered_algo:
                color = BUTTON_HOVER

            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            text_surface = self.font.render(button['text'], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered_algo = None
            for button in self.buttons:
                if button['rect'].collidepoint(event.pos):
                    self.hovered_algo = button['algo']

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        self.active_algo = button['algo']
                        return button['algo']
        return None
