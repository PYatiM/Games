import random

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (
            random.randint(1, self.height - 2),
            random.randint(1, self.width - 2)
        )