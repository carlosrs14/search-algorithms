import asyncio
import pygame
from utils.reader import GraphReader

async def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    
    # Test Data Loading
    data_file = 'data/chn31.txt'
    await asyncio.sleep(0) # Let pygame init
    
    try:
        reader = GraphReader(data_file)
        cities = reader.get_cities()
        screen.fill((0, 0, 255)) # Blue screen = data successfully loaded!
    except Exception as e:
        print("DATA LOAD FAILED:", e)
        screen.fill((255, 255, 0)) # Yellow screen = Data error!
        
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            pass
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())