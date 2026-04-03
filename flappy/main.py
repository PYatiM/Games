import pygame
from settings import WIDTH, HEIGHT, FPS
from game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

game = Game()

while game.running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.bird.jump()

    game.update()
    game.draw(screen)

    pygame.display.flip()

pygame.quit()