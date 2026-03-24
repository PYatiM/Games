import curses
from snake import Snake
from food import Food
import config

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.snake = Snake()
        self.food = Food(config.WIDTH, config.HEIGHT)
        self.score = 0

    def process_input(self):
        key = self.stdscr.getch()

        directions = {
            curses.KEY_UP: (-1, 0),
            curses.KEY_DOWN: (1, 0),
            curses.KEY_LEFT: (0, -1),
            curses.KEY_RIGHT: (0, 1),
        }

        if key in directions:
            self.snake.change_direction(directions[key])

    def update(self):
        self.snake.move()
        head = self.snake.get_head()

        # collision with food
        if head == self.food.position:
            self.snake.grow()
            self.food.spawn()
            self.score += 1

        # collision with walls
        y, x = head
        if y <= 0 or y >= config.HEIGHT-1 or x <= 0 or x >= config.WIDTH-1:
            return False

        # collision with itself
        if head in self.snake.body[1:]:
            return False

        return True

    def draw(self):
        self.stdscr.clear()

        # borders
        for x in range(config.WIDTH):
            self.stdscr.addstr(0, x, "#")
            self.stdscr.addstr(config.HEIGHT-1, x, "#")
        for y in range(config.HEIGHT):
            self.stdscr.addstr(y, 0, "#")
            self.stdscr.addstr(y, config.WIDTH-1, "#")

        # snake
        for y, x in self.snake.body:
            self.stdscr.addstr(y, x, "O")

        # food
        y, x = self.food.position
        self.stdscr.addstr(y, x, "*")

        self.stdscr.addstr(0, 2, f" Score: {self.score} ")
        self.stdscr.refresh()

    def run(self):
        self.stdscr.nodelay(1)
        self.stdscr.timeout(config.SPEED)

        while True:
            self.process_input()
            if not self.update():
                break
            self.draw()