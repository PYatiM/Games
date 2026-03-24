class Snake:
    def __init__(self):
        self.body = [(10, 10), (10, 9), (10, 8)]
        self.direction = (0, 1)  # moving right

    def move(self):
        head_y, head_x = self.body[0]
        dy, dx = self.direction
        new_head = (head_y + dy, head_x + dx)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_dir):
        self.direction = new_dir

    def get_head(self):
        return self.body[0]