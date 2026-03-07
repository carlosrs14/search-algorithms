import pygame
import asyncio
import sys
from utils.colors import BACKGROUND
from gui.menu import Menu
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.aStar import AStar
from algorithms.dijkstra import Dijkstra
from algorithms.greedy import Greedy

class Window:
    def __init__(self, sizes, title, game_map, graph, cities, start_node, end_node):
        pygame.init()
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        
        # Sidebar layout
        self.sidebar_width = 300
        self.map_width = self.width - self.sidebar_width
        
        # Update map width
        self.game_map = game_map
        self.game_map.width = self.map_width
        self.game_map.scale_x = (self.map_width - 2 * self.game_map.padding)
        
        self.graph = graph
        self.cities = cities
        self.start_node = start_node
        self.end_node = end_node
        
        menu_rect = pygame.Rect(self.map_width, 0, self.sidebar_width, self.height)
        self.menu = Menu(menu_rect)

        self.algo_generator = None
        self.is_paused = False
        
        self.frontier = set()
        self.visited = set()
        self.current_node = None
        self.path = []

    def _run_algorithm(self, algo_name):
        # Reset state
        self.frontier = set()
        self.visited = set()
        self.current_node = None
        self.path = []
        self.algo_generator = None
        
        if algo_name == 'BFS':
            algo = BFS(self.graph, self.start_node, self.end_node)
        elif algo_name == 'DFS':
            algo = DFS(self.graph, self.start_node, self.end_node)
        elif algo_name == 'A*':
            algo = AStar(self.graph, self.start_node, self.end_node, self.cities)
        elif algo_name == 'Dijkstra':
            algo = Dijkstra(self.graph, self.start_node, self.end_node)
        elif algo_name == 'Greedy':
            algo = Greedy(self.graph, self.start_node, self.end_node, self.cities)
        else:
            return
        
        self.algo_generator = algo.solve()
        self.is_paused = False

    async def start(self):
        running = True
        
        while running:
            dt = self.clock.tick(self.menu.fps)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                selected_algo = self.menu.handle_event(event)
                if selected_algo:
                    self._run_algorithm(selected_algo)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Check if click is on map
                    if pos[0] < self.map_width:
                        clicked_node = self.game_map.get_city_at_pos(pos)
                        if clicked_node is not None:
                            if event.button == 1: # Left click -> Start node
                                self.start_node = clicked_node
                                if self.menu.active_algo:
                                    self._run_algorithm(self.menu.active_algo)
                                else:
                                    # Reset state purely
                                    self._run_algorithm(None)
                            elif event.button == 3: # Right click -> End node
                                self.end_node = clicked_node
                                if self.menu.active_algo:
                                    self._run_algorithm(self.menu.active_algo)
                                else:
                                    self._run_algorithm(None)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.is_paused = not self.is_paused

            if self.algo_generator and not self.is_paused:
                # Step the generator once per frame
                try:
                    state = next(self.algo_generator)
                    if state:
                        self.frontier, self.visited, self.current_node, self.path = state
                except StopIteration:
                    self.algo_generator = None

            self.screen.fill(BACKGROUND)
            
            # Draw map
            self.game_map.draw(
                self.screen, 
                self.graph, 
                self.frontier, 
                self.visited, 
                self.current_node, 
                self.path, 
                self.start_node, 
                self.end_node
            )
            
            # Draw menu
            self.menu.draw(self.screen)

            pygame.display.update()
            await asyncio.sleep(0)
            
        pygame.quit()
        sys.exit()
