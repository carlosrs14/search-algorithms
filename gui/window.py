import pygame
import sys
from utils.colors import WHITE, BLACK, RED
from gui.menu import Menu
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.aStar import AStar

class Window:
    def __init__(self, sizes, title, game_map, graph, cities, start_node, end_node):
        pygame.init()
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        self.game_map = game_map
        self.graph = graph
        self.cities = cities
        self.start_node = start_node
        self.end_node = end_node
        self.path = None

        self.state = 'MENU' # States: MENU, VISUALIZING
        self.menu = Menu(self.width, self.height)

        # Back button
        self.back_button_rect = pygame.Rect(10, 10, 100, 40)
        self.font = pygame.font.Font(None, 30)

    def _run_algorithm(self, algo_name):
        if algo_name == 'BFS':
            algo = BFS(self.graph, self.start_node, self.end_node)
        elif algo_name == 'DFS':
            algo = DFS(self.graph, self.start_node, self.end_node)
        elif algo_name == 'A*':
            algo = AStar(self.graph, self.start_node, self.end_node, self.cities)
        else:
            return
        
        self.path = algo.solve()
        self.state = 'VISUALIZING'

    def start(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == 'MENU':
                    selected_algo = self.menu.handle_event(event)
                    if selected_algo:
                        self._run_algorithm(selected_algo)
                elif self.state == 'VISUALIZING':
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.back_button_rect.collidepoint(event.pos):
                            self.state = 'MENU'
                            self.path = None # Clear path

            self.screen.fill(WHITE)

            if self.state == 'MENU':
                self.menu.draw(self.screen)
            elif self.state == 'VISUALIZING':
                self.game_map.draw(self.screen, self.path, self.start_node, self.end_node)
                # Draw back button
                pygame.draw.rect(self.screen, RED, self.back_button_rect)
                back_text = self.font.render("Back", True, WHITE)
                text_rect = back_text.get_rect(center=self.back_button_rect.center)
                self.screen.blit(back_text, text_rect)

            pygame.display.update()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
