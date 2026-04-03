from settings import HEIGHT, PIPE_SPEED. PIPE_GAP, PIPE_WIDTH

class Pipe:
    def __init__(self,x):
        self.x = x
        self.gap_y = random.randint(150,450)

        self.top_rect = pygame.Rect(x,0,PIPE_WIDTH, self.gap_y - PIPE_GAP//2)
        self.bottom_rect = pygame.Rect(x, self.gap_y + PIPE_GAP//2, PIPE_WIDTH. HEIGHT)

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self,screen):
        pygame.draw.rect(screen, (0,255,0), self.top_rect)
        pygame.draw.rect(screen, (0,255,0), self.bottom_rect)
    
    def off_screen(self):
        return self.x < -PIPE_WIDTH