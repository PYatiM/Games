# Push the Block Game (Sokoban-Style)

A classic puzzle game where you push blocks to target locations. Features randomized maps, multiple difficulty levels, and both GUI and terminal/console modes.

## Features

- 🎮 **Two Play Modes**: Graphical (GUI) and Terminal/Console
- 🎲 **Random Map Generation**: Every game is different
- 🎯 **4 Difficulty Levels**: Easy, Medium, Hard, Expert
- ↩️ **Undo System**: Take back your moves
- 🏆 **Win Detection**: Automatically detects when you've won
- 🎨 **Colorful Graphics**: Nice visual design in GUI mode

## Game Rules

1. Push all boxes ($) onto the target locations (.)
2. You can only push boxes, not pull them
3. You can only push one box at a time
4. Plan your moves carefully - boxes can get stuck!

## Python Version

### Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python)

### How to Run

**GUI Mode (Default):**
```bash
python3 push_block_game.py
```

**Terminal Mode:**
```bash
python3 push_block_game.py
# Then select option 2 when prompted
```

**Direct Terminal Launch:**
```python
python3 -c "from push_block_game import play_terminal; play_terminal()"
```

### Controls (Python)
- **Movement**: WASD or Arrow Keys
- **Undo**: U
- **Restart**: R
- **New Game**: N (GUI only)
- **Quit**: Q (Terminal only)

## Java Version

### Requirements
- Java 8 or higher (JDK)
- Java Swing (included in standard JDK)

### How to Compile
```bash
javac PushBlockGame.java GameGUI.java GamePanel.java
```

### How to Run

**GUI Mode (Default):**
```bash
java PushBlockGame
```

**Console Mode:**
```bash
java PushBlockGame
# Then select option 2 when prompted
```

### Controls (Java)
- **Movement**: WASD or Arrow Keys
- **Undo**: U
- **Restart**: R
- **New Game**: N (GUI only)
- **Quit**: Q (Console only)

## Difficulty Levels

| Level  | Boxes | Map Complexity | Challenge                    |
|--------|-------|----------------|------------------------------|
| Easy   | 2     | Low            | Good for learning            |
| Medium | 3     | Moderate       | Balanced challenge           |
| Hard   | 4     | High           | Requires planning            |
| Expert | 5     | Very High      | For puzzle masters           |

## Game Symbols

```
@  = Player
#  = Wall
$  = Box
.  = Target location
*  = Box on target (GREEN in GUI)
+  = Player on target
```

## Tips & Strategies

1. **Plan Ahead**: Think several moves in advance
2. **Corner Awareness**: Boxes pushed into corners can't be retrieved
3. **Target Proximity**: Try to keep boxes near their target zones
4. **Use Undo**: Don't be afraid to experiment and undo
5. **Wall Hugging**: Sometimes pushing boxes along walls is safer

## Screenshots

**GUI Mode:**
- Clean, colorful interface
- Visual feedback for boxes on targets (green)
- Move counter and progress tracker

**Terminal Mode:**
- Classic ASCII graphics
- Works on any terminal
- Perfect for SSH sessions

## Code Structure

### Python (`push_block_game.py`)
- `PushBlockGame` class: Core game logic
- `play_gui()`: Tkinter GUI implementation
- `play_terminal()`: Console-based gameplay
- Random map generation with solvability checking

### Java (`PushBlockGame.java`)
- `PushBlockGame` class: Core game logic
- `GameGUI` class: Swing GUI implementation
- `GamePanel` class: Custom rendering
- `playConsole()`: Console-based gameplay

## Algorithm Highlights

### Map Generation
1. Create bordered play area
2. Add random walls based on difficulty
3. Place player, boxes, and targets
4. Verify solvability using BFS (Breadth-First Search)
5. Retry if unsolvable (max 100 attempts)

### Move Validation
1. Check boundaries and walls
2. Detect box collision
3. Calculate box push position
4. Validate box push legality
5. Update game state

### Win Condition
- All boxes must be on target positions
- Uses set equality check for efficiency

## Customization

### Python
```python
# Create custom game
game = PushBlockGame(
    difficulty='hard',
    width=12,      # Map width
    height=10      # Map height
)
```

### Java
```java
// Create custom game
PushBlockGame game = new PushBlockGame(
    "hard",  // difficulty
    12,      // width
    10       // height
);
```

## Troubleshooting

**Python - tkinter not found:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (should be included)
# Windows (should be included with Python)
```

**Java - Compilation errors:**
```bash
# Make sure you're using Java 8+
java -version

# Compile all files together
javac *.java
```

**Terminal mode not clearing screen:**
- This is normal on some terminals
- The game will still work, just with scrolling

## Learning Outcomes

This project demonstrates:
- **Algorithms**: BFS for pathfinding, random generation
- **Data Structures**: Sets, stacks (for undo), 2D arrays
- **Game Logic**: State management, win conditions, move validation
- **GUI Programming**: Event handling, custom rendering
- **Object-Oriented Design**: Encapsulation, separation of concerns

## Future Enhancements

Ideas for extending the game:
- [ ] Save/load game states
- [ ] Level editor
- [ ] Hint system
- [ ] Solution replay
- [ ] Multiplayer mode
- [ ] Time challenges
- [ ] Custom themes/skins

## License

Educational purposes - feel free to modify and learn from this code!

## Author

Created as an educational example demonstrating game development, algorithms, and GUI programming in Python and Java.

---

**Enjoy the game! 🎮**