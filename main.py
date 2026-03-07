import asyncio
import pygame
from gui.window import Window
from utils import sizes
from utils.reader import GraphReader
from gui.map import Map

async def main():
    start_node = 0
    end_node = 30
    data_file = 'data/chn31.txt'

    await asyncio.sleep(0) # Let pygame init
    reader = GraphReader(data_file)
    cities = reader.get_cities()
    graph = reader.get_graph()

    await asyncio.sleep(0) # Yield before creating heavy window
    game_map = Map(cities, sizes.REGULAR[0], sizes.REGULAR[1])
    window = Window(
        sizes.REGULAR, 
        "Algorithm Visualizer", 
        game_map=game_map, 
        graph=graph, 
        cities=cities, 
        start_node=start_node, 
        end_node=end_node
    )
    await window.start()

if __name__ == "__main__":
    asyncio.run(main())