import pygame
from utils.colors import PANEL_BG, BUTTON_BG, BUTTON_HOVER, BUTTON_ACTIVE, TEXT_COLOR

class Menu:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.title_font.set_bold(True)
        self.instructions_font = pygame.font.Font(None, 16)
        self.speed_font = pygame.font.Font(None, 18)
        self.speed_font.set_bold(True)

        self.algorithms = ['BFS', 'DFS', 'A*', 'Dijkstra', 'Greedy']
        self.datasets = ['chn31', 'att48', 'chn144']
        self.buttons = []
        self.active_algo = None
        self.active_dataset = 'chn31'
        
        self.dataset_title_y = 0
        self.speed_label_y = 0
        
        self.hovered_btn = None
        
        self.fps_options = [1, 5, 15, 30, 60, 120]
        self.fps_idx = 4
        self.fps = self.fps_options[self.fps_idx]
        
        self._create_buttons()

    def _create_buttons(self):
        self.buttons.clear()
        button_width = self.rect.width - 40
        button_height = 40
        x = self.rect.x + 20
        y_start = self.rect.y + 70
        y_gap = 45

        for i, algo in enumerate(self.algorithms):
            y = y_start + i * y_gap
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append({'rect': rect, 'text': algo, 'action': algo, 'type': 'algo'})

        # Datasets
        dataset_y_label = y_start + len(self.algorithms) * y_gap + 10
        self.dataset_title_y = dataset_y_label
        dataset_y_start = dataset_y_label + 40
        for i, ds in enumerate(self.datasets):
            y = dataset_y_start + i * y_gap
            rect = pygame.Rect(x, y, button_width, button_height)
            self.buttons.append({'rect': rect, 'text': ds, 'action': ds, 'type': 'dataset'})

        # Speed controls
        speed_y = dataset_y_start + len(self.datasets) * y_gap + 20
        self.speed_label_y = speed_y - 25
        half_btn_width = (button_width - 10) // 2
        
        slow_rect = pygame.Rect(x, speed_y, half_btn_width, button_height)
        fast_rect = pygame.Rect(x + half_btn_width + 10, speed_y, half_btn_width, button_height)
        
        self.buttons.append({'rect': slow_rect, 'text': 'Slower', 'action': 'speed_down', 'type': 'speed'})
        self.buttons.append({'rect': fast_rect, 'text': 'Faster', 'action': 'speed_up', 'type': 'speed'})

    def draw(self, screen):
        # Draw panel background
        pygame.draw.rect(screen, PANEL_BG, self.rect)
        pygame.draw.line(screen, (50, 50, 60), (self.rect.x, 0), (self.rect.x, self.rect.height), 2)

        # Draw title
        title_surface = self.title_font.render("Algorithms", True, TEXT_COLOR)
        screen.blit(title_surface, (self.rect.x + 20, self.rect.y + 20))

        # Instructions
        inst_surf1 = self.instructions_font.render("Left Click Node: Set Start", True, (150, 150, 160))
        inst_surf2 = self.instructions_font.render("Right Click Node: Set End", True, (150, 150, 160))
        inst_surf3 = self.instructions_font.render("Space: Play/Pause", True, (150, 150, 160))
        
        dy = self.rect.height - 100
        screen.blit(inst_surf1, (self.rect.x + 20, dy))
        screen.blit(inst_surf2, (self.rect.x + 20, dy + 25))
        screen.blit(inst_surf3, (self.rect.x + 20, dy + 50))

        # Dataset Title
        dataset_title = self.title_font.render("Datasets", True, TEXT_COLOR)
        screen.blit(dataset_title, (self.rect.x + 20, self.dataset_title_y))

        # Speed Label
        speed_label = self.speed_font.render(f"Speed: {self.fps} FPS", True, TEXT_COLOR)
        # Position it above the speed buttons
        screen.blit(speed_label, (self.rect.x + 20, self.speed_label_y))

        # Draw buttons
        for button in self.buttons:
            color = BUTTON_BG
            if button['type'] == 'algo' and button['action'] == self.active_algo:
                color = BUTTON_ACTIVE
            elif button['type'] == 'dataset' and button['action'] == self.active_dataset:
                color = BUTTON_ACTIVE
            elif button == self.hovered_btn:
                color = BUTTON_HOVER

            pygame.draw.rect(screen, color, button['rect'], border_radius=8)
            text_surface = self.font.render(button['text'], True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=button['rect'].center)
            screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered_btn = None
            for button in self.buttons:
                if button['rect'].collidepoint(event.pos):
                    self.hovered_btn = button

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                for button in self.buttons:
                    if button['rect'].collidepoint(event.pos):
                        if button['type'] == 'algo':
                            self.active_algo = button['action']
                            return {'type': 'algo', 'value': button['action']}
                        elif button['type'] == 'dataset':
                            self.active_dataset = button['action']
                            return {'type': 'dataset', 'value': button['action']}
                        elif button['type'] == 'speed':
                            if button['action'] == 'speed_up':
                                self.fps_idx = min(len(self.fps_options) - 1, self.fps_idx + 1)
                            elif button['action'] == 'speed_down':
                                self.fps_idx = max(0, self.fps_idx - 1)
                            self.fps = self.fps_options[self.fps_idx]
                            return None
        return None
