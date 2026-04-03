import pygame 
from bird import Bird
from pipe import Pipe
from settings import WIDTH

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipe = [pipe(400)]
        self.score = 0
        self.frame_count = 0
        self.running = True

    def spawn_pipe(self):
        if self.frame_count % 90 == 0:
            self.pipes.append(Pipe(WIDTH))

    def update(self):
        self.frame_count += 1

        self.bird.update()

        for pipe in self.pipes:
            pipe.update()

        self.spawn_pipe()
            
        self.pipes = [p for p in self.pipes if not p.off_screen()]

        self.check_collision()

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.running = False

        if self.bird.y < 0 or self.bird.y > self.running > 600:
            self.running = False

    def draw(self, screen):
        screen.fill((135, 206, 235)) #sky vlue color

        self.bird.draw(screen)
        for pipe in self.pipes:
            pipe.draw(screen)

            