import pygame
from settings import GRAVITY, JUMP_STRENGTH

class Bird:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.vel = 0
        self.rect = pygame.Rect(self.x,self.y,30,30)  #creating rectangular image

    def jump(self):
        self.vel = JUMP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y) # updating the rectangular image

    def draw(self,screen):
        pygame.draw.rect(screen, (255,255,0), self.rect)

    