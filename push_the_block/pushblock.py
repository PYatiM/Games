import random
import sys
from collections import deque
from copy import deepcopy
 
# Game symbols
PLAYER = '@'
WALL = '#'
BOX = '$'
TARGET = '.'
BOX_ON_TARGET = '*'
PLAYER_ON_TARGET = '+'
EMPTY = ' '
 
 
class PushBlockGame:
    def __init__(self, difficulty='medium', width=10, height=8):
        self.difficulty = difficulty
        self.width = width
        self.height = height
        self.moves = 0
        self.history = []  # For undo functionality
        
        # Set difficulty parameters
        difficulty_settings = {
            'easy': {'boxes': 2, 'wall_density': 0.15},
            'medium': {'boxes': 3, 'wall_density': 0.20},
            'hard': {'boxes': 4, 'wall_density': 0.25},
            'expert': {'boxes': 5, 'wall_density': 0.30}
        }
        
        settings = difficulty_settings.get(difficulty, difficulty_settings['medium'])
        self.num_boxes = settings['boxes']
        self.wall_density = settings['wall_density']
        
        self.generate_map()
    
    def generate_map(self):
        """Generate a random solvable map"""
        max_attempts = 100
        
        for attempt in range(max_attempts):
            self.grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
            
            # Add borders
            for i in range(self.height):
                self.grid[i][0] = WALL
                self.grid[i][self.width - 1] = WALL
            for j in range(self.width):
                self.grid[0][j] = WALL
                self.grid[self.height - 1][j] = WALL
            
            # Add random internal walls
            for i in range(2, self.height - 2):
                for j in range(2, self.width - 2):
                    if random.random() < self.wall_density:
                        self.grid[i][j] = WALL
            
            # Find open spaces
            open_spaces = []
            for i in range(1, self.height - 1):
                for j in range(1, self.width - 1):
                    if self.grid[i][j] == EMPTY:
                        open_spaces.append((i, j))
            
            if len(open_spaces) < self.num_boxes * 2 + 1:
                continue
            
            # Randomly place player, boxes, and targets
            random.shuffle(open_spaces)
            
            self.player_pos = open_spaces[0]
            self.boxes = set(open_spaces[1:1 + self.num_boxes])
            self.targets = set(open_spaces[1 + self.num_boxes:1 + 2 * self.num_boxes])
            
            # Verify solvability (basic check: targets and boxes are reachable)
            if self.is_valid_map():
                self.update_grid()
                return
        
        # Fallback: create a simple valid map
        self.create_simple_map()
    
    def create_simple_map(self):
        """Create a simple guaranteed solvable map"""
        self.grid = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        
        # Create a large open area
        for i in range(2, self.height - 2):
            for j in range(2, self.width - 2):
                self.grid[i][j] = EMPTY
        
        # Place elements in known good positions
        self.player_pos = (3, 3)
        self.boxes = {(4, 4), (4, 5)}
        self.targets = {(self.height - 3, self.width - 3), (self.height - 3, self.width - 4)}
        self.num_boxes = len(self.boxes)
        
        self.update_grid()
    
    def is_valid_map(self):
        """Check if the map is potentially solvable"""
        # Check that player can reach all boxes and targets
        reachable = self.get_reachable_positions(self.player_pos)
        
        for box in self.boxes:
            if box not in reachable:
                return False
        
        for target in self.targets:
            if target not in reachable:
                return False
        
        return True
    
    def get_reachable_positions(self, start):
        """BFS to find all positions reachable from start"""
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            y, x = queue.popleft()
            
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                
                if (ny, nx) not in visited and \
                   0 <= ny < self.height and 0 <= nx < self.width and \
                   self.grid[ny][nx] != WALL and \
                   (ny, nx) not in self.boxes:
                    visited.add((ny, nx))
                    queue.append((ny, nx))
        
        return visited
    
    def update_grid(self):
        """Update grid representation based on current state"""
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] != WALL:
                    self.grid[i][j] = EMPTY
        
        # Place targets
        for pos in self.targets:
            self.grid[pos[0]][pos[1]] = TARGET
        
        # Place boxes
        for pos in self.boxes:
            if pos in self.targets:
                self.grid[pos[0]][pos[1]] = BOX_ON_TARGET
            else:
                self.grid[pos[0]][pos[1]] = BOX
        
        # Place player
        if self.player_pos in self.targets:
            self.grid[self.player_pos[0]][self.player_pos[1]] = PLAYER_ON_TARGET
        else:
            self.grid[self.player_pos[0]][self.player_pos[1]] = PLAYER
    
    def move(self, direction):
        """Attempt to move player in given direction"""
        # Save state for undo
        self.history.append({
            'player_pos': self.player_pos,
            'boxes': self.boxes.copy(),
            'moves': self.moves
        })
        
        dy, dx = direction
        new_y, new_x = self.player_pos[0] + dy, self.player_pos[1] + dx
        
        # Check boundaries
        if not (0 <= new_y < self.height and 0 <= new_x < self.width):
            self.history.pop()
            return False
        
        # Check wall
        if self.grid[new_y][new_x] == WALL:
            self.history.pop()
            return False
        
        # Check if there's a box
        if (new_y, new_x) in self.boxes:
            # Try to push the box
            box_new_y, box_new_x = new_y + dy, new_x + dx
            
            # Check if box can be pushed
            if not (0 <= box_new_y < self.height and 0 <= box_new_x < self.width):
                self.history.pop()
                return False
            
            if self.grid[box_new_y][box_new_x] == WALL or (box_new_y, box_new_x) in self.boxes:
                self.history.pop()
                return False
            
            # Push the box
            self.boxes.remove((new_y, new_x))
            self.boxes.add((box_new_y, box_new_x))
        
        # Move player
        self.player_pos = (new_y, new_x)
        self.moves += 1
        self.update_grid()
        return True
    
    def undo(self):
        """Undo last move"""
        if self.history:
            state = self.history.pop()
            self.player_pos = state['player_pos']
            self.boxes = state['boxes']
            self.moves = state['moves']
            self.update_grid()
            return True
        return False
    
    def is_won(self):
        """Check if all boxes are on targets"""
        return self.boxes == self.targets
    
    def get_display_string(self):
        """Get string representation of the game"""
        result = [f"\nMoves: {self.moves} | Difficulty: {self.difficulty.upper()}\n"]
        result.append("=" * (self.width + 2) + "\n")
        
        for row in self.grid:
            result.append("".join(row) + "\n")
        
        result.append("=" * (self.width + 2) + "\n")
        result.append("\nControls: WASD or Arrow keys to move, U to undo, R to restart, Q to quit\n")
        result.append(f"Boxes on targets: {len(self.boxes & self.targets)}/{self.num_boxes}\n")
        
        return "".join(result)
 
 
def play_terminal():
    """Play game in terminal mode"""
    print("\n=== PUSH THE BLOCK - Terminal Mode ===\n")
    print("Select difficulty:")
    print("1. Easy (2 boxes)")
    print("2. Medium (3 boxes)")
    print("3. Hard (4 boxes)")
    print("4. Expert (5 boxes)")
    
    choice = input("\nEnter choice (1-4) [default: 2]: ").strip()
    
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'expert'}
    difficulty = difficulty_map.get(choice, 'medium')
    
    game = PushBlockGame(difficulty=difficulty)
    
    direction_map = {
        'w': (-1, 0), 'W': (-1, 0),
        's': (1, 0), 'S': (1, 0),
        'a': (0, -1), 'A': (0, -1),
        'd': (0, 1), 'D': (0, 1),
    }
    
    while True:
        print("\033[2J\033[H")  # Clear screen
        print(game.get_display_string())
        
        if game.is_won():
            print(f"\n🎉 CONGRATULATIONS! You won in {game.moves} moves! 🎉\n")
            
            play_again = input("Play again? (y/n): ").strip().lower()
            if play_again == 'y':
                game = PushBlockGame(difficulty=difficulty)
            else:
                break
        
        move = input("Your move: ").strip().lower()
        
        if move in ['q', 'quit', 'exit']:
            print("Thanks for playing!")
            break
        elif move in ['r', 'restart']:
            game = PushBlockGame(difficulty=difficulty)
        elif move in ['u', 'undo']:
            game.undo()
        elif move in direction_map:
            game.move(direction_map[move])
        else:
            print("Invalid move! Use W/A/S/D")
            input("Press Enter to continue...")
 
 
def play_gui():
    """Play game in GUI mode using tkinter"""
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        print("Tkinter not available. Please install python3-tk or use terminal mode.")
        return
    
    class GameGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Push the Block")
            self.game = None
            self.cell_size = 40
            
            self.show_difficulty_menu()
        
        def show_difficulty_menu(self):
            """Show difficulty selection menu"""
            menu_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
            menu_frame.pack(expand=True, fill='both')
            
            tk.Label(menu_frame, text="PUSH THE BLOCK", 
                    font=('Arial', 24, 'bold'), bg='#2c3e50', fg='white').pack(pady=20)
            
            tk.Label(menu_frame, text="Select Difficulty:", 
                    font=('Arial', 14), bg='#2c3e50', fg='white').pack(pady=10)
            
            difficulties = [
                ('Easy (2 boxes)', 'easy'),
                ('Medium (3 boxes)', 'medium'),
                ('Hard (4 boxes)', 'hard'),
                ('Expert (5 boxes)', 'expert')
            ]
            
            for text, diff in difficulties:
                tk.Button(menu_frame, text=text, font=('Arial', 12),
                         command=lambda d=diff: self.start_game(d),
                         bg='#3498db', fg='white', padx=20, pady=10,
                         relief='flat', cursor='hand2').pack(pady=5)
        
        def start_game(self, difficulty):
            """Start a new game with selected difficulty"""
            for widget in self.root.winfo_children():
                widget.destroy()
            
            self.game = PushBlockGame(difficulty=difficulty)
            
            # Info frame
            self.info_frame = tk.Frame(self.root, bg='#34495e', padx=10, pady=10)
            self.info_frame.pack(fill='x')
            
            self.moves_label = tk.Label(self.info_frame, text=f"Moves: 0", 
                                       font=('Arial', 12, 'bold'), bg='#34495e', fg='white')
            self.moves_label.pack(side='left', padx=10)
            
            self.status_label = tk.Label(self.info_frame, 
                                        text=f"Difficulty: {difficulty.upper()}", 
                                        font=('Arial', 12), bg='#34495e', fg='white')
            self.status_label.pack(side='left', padx=10)
            
            # Canvas for game
            canvas_width = self.game.width * self.cell_size
            canvas_height = self.game.height * self.cell_size
            
            self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height, 
                                   bg='#1a1a1a', highlightthickness=0)
            self.canvas.pack(padx=10, pady=10)
            
            # Button frame
            button_frame = tk.Frame(self.root, bg='#34495e', padx=10, pady=10)
            button_frame.pack(fill='x')
            
            tk.Button(button_frame, text="Undo (U)", command=self.undo,
                     bg='#e74c3c', fg='white', font=('Arial', 10), 
                     relief='flat', padx=10, pady=5).pack(side='left', padx=5)
            
            tk.Button(button_frame, text="Restart (R)", command=lambda: self.start_game(difficulty),
                     bg='#f39c12', fg='white', font=('Arial', 10), 
                     relief='flat', padx=10, pady=5).pack(side='left', padx=5)
            
            tk.Button(button_frame, text="New Game (N)", command=self.show_difficulty_menu,
                     bg='#3498db', fg='white', font=('Arial', 10), 
                     relief='flat', padx=10, pady=5).pack(side='left', padx=5)
            
            # Bind keys
            self.root.bind('<Up>', lambda e: self.move((-1, 0)))
            self.root.bind('<Down>', lambda e: self.move((1, 0)))
            self.root.bind('<Left>', lambda e: self.move((0, -1)))
            self.root.bind('<Right>', lambda e: self.move((0, 1)))
            self.root.bind('w', lambda e: self.move((-1, 0)))
            self.root.bind('s', lambda e: self.move((1, 0)))
            self.root.bind('a', lambda e: self.move((0, -1)))
            self.root.bind('d', lambda e: self.move((0, 1)))
            self.root.bind('u', lambda e: self.undo())
            self.root.bind('r', lambda e: self.start_game(difficulty))
            self.root.bind('n', lambda e: self.show_difficulty_menu())
            
            self.draw_game()
        
        def draw_game(self):
            """Draw the game board"""
            self.canvas.delete('all')
            
            colors = {
                WALL: '#7f8c8d',
                EMPTY: '#1a1a1a',
                TARGET: '#f39c12',
                BOX: '#c0392b',
                BOX_ON_TARGET: '#27ae60',
                PLAYER: '#3498db',
                PLAYER_ON_TARGET: '#9b59b6'
            }
            
            for i in range(self.game.height):
                for j in range(self.game.width):
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    
                    cell = self.game.grid[i][j]
                    
                    # Draw background
                    if cell == TARGET or cell == PLAYER_ON_TARGET:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                    fill='#f39c12', outline='#e67e22')
                    else:
                        self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                    fill='#2c3e50', outline='#34495e')
                    
                    # Draw entity
                    if cell == WALL:
                        self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, 
                                                    fill=colors[WALL], outline='')
                    elif cell == BOX or cell == BOX_ON_TARGET:
                        color = colors[cell]
                        self.canvas.create_rectangle(x1+5, y1+5, x2-5, y2-5, 
                                                    fill=color, outline='white', width=2)
                    elif cell == PLAYER or cell == PLAYER_ON_TARGET:
                        self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, 
                                              fill=colors[PLAYER], outline='white', width=2)
            
            self.moves_label.config(text=f"Moves: {self.game.moves}")
            boxes_on_targets = len(self.game.boxes & self.game.targets)
            self.status_label.config(text=f"Boxes: {boxes_on_targets}/{self.game.num_boxes}")
        
        def move(self, direction):
            """Handle player movement"""
            if self.game.move(direction):
                self.draw_game()
                
                if self.game.is_won():
                    messagebox.showinfo("Congratulations!", 
                                      f"You won in {self.game.moves} moves!")
        
        def undo(self):
            """Undo last move"""
            if self.game.undo():
                self.draw_game()
    
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
 
 
def main():
    """Main entry point"""
    print("\n=== PUSH THE BLOCK ===\n")
    print("Choose mode:")
    print("1. GUI (Graphical)")
    print("2. Terminal")
    
    choice = input("\nEnter choice (1-2) [default: 1]: ").strip()
    
    if choice == '2':
        play_terminal()
    else:
        play_gui()
 
 
if __name__ == '__main__':
    main()