import asyncio
import pygame

async def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    screen.fill((255, 0, 0)) # Red screen to prove execution
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            pass
        screen.fill((0, 255, 0)) # Green screen
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())