import pygame
import globals
from game import Game

pygame.init()

screen = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT))
pygame.display.set_caption("SpaceShooterAI Example")
clock = pygame.time.Clock()

globals.FONT = pygame.font.SysFont(None, 18)

game = Game()

running = True
while running:
    dt = clock.tick(60) / 1000.0

    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_TAB:
                globals.SHOW_DEBUG = not globals.SHOW_DEBUG

    game.update(dt)
    game.draw(screen)

    pygame.display.flip()

pygame.quit()
