import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;
import java.util.List;

public class PushBlockGame {
    // Game symbols
    private static final char PLAYER = '@';
    private static final char WALL = '#';
    private static final char BOX = '$';
    private static final char TARGET = '.';
    private static final char BOX_ON_TARGET = '*';
    private static final char PLAYER_ON_TARGET = '+';
    private static final char EMPTY = ' ';
    
    private char[][] grid;
    private int width;
    private int height;
    private Point playerPos;
    private Set<Point> boxes;
    private Set<Point> targets;
    private int numBoxes;
    private int moves;
    private String difficulty;
    private double wallDensity;
    private Stack<GameState> history;
    
    public PushBlockGame(String difficulty, int width, int height) {
        this.difficulty = difficulty;
        this.width = width;
        this.height = height;
        this.moves = 0;
        this.history = new Stack<>();
        
        // Set difficulty parameters
        Map<String, DifficultySettings> settings = new HashMap<>();
        settings.put("easy", new DifficultySettings(2, 0.15));
        settings.put("medium", new DifficultySettings(3, 0.20));
        settings.put("hard", new DifficultySettings(4, 0.25));
        settings.put("expert", new DifficultySettings(5, 0.30));
        
        DifficultySettings diff = settings.getOrDefault(difficulty, settings.get("medium"));
        this.numBoxes = diff.boxes;
        this.wallDensity = diff.wallDensity;
        
        generateMap();
    }
    
    private void generateMap() {
        int maxAttempts = 100;
        Random rand = new Random();
        
        for (int attempt = 0; attempt < maxAttempts; attempt++) {
            grid = new char[height][width];
            
            // Initialize with empty spaces
            for (int i = 0; i < height; i++) {
                for (int j = 0; j < width; j++) {
                    grid[i][j] = EMPTY;
                }
            }
            
            // Add borders
            for (int i = 0; i < height; i++) {
                grid[i][0] = WALL;
                grid[i][width - 1] = WALL;
            }
            for (int j = 0; j < width; j++) {
                grid[0][j] = WALL;
                grid[height - 1][j] = WALL;
            }
            
            // Add random internal walls
            for (int i = 2; i < height - 2; i++) {
                for (int j = 2; j < width - 2; j++) {
                    if (rand.nextDouble() < wallDensity) {
                        grid[i][j] = WALL;
                    }
                }
            }
            
            // Find open spaces
            List<Point> openSpaces = new ArrayList<>();
            for (int i = 1; i < height - 1; i++) {
                for (int j = 1; j < width - 1; j++) {
                    if (grid[i][j] == EMPTY) {
                        openSpaces.add(new Point(j, i));
                    }
                }
            }
            
            if (openSpaces.size() < numBoxes * 2 + 1) {
                continue;
            }
            
            // Randomly place player, boxes, and targets
            Collections.shuffle(openSpaces);
            
            playerPos = openSpaces.get(0);
            boxes = new HashSet<>();
            targets = new HashSet<>();
            
            for (int i = 1; i <= numBoxes; i++) {
                boxes.add(openSpaces.get(i));
            }
            for (int i = numBoxes + 1; i <= 2 * numBoxes; i++) {
                targets.add(openSpaces.get(i));
            }
            
            if (isValidMap()) {
                updateGrid();
                return;
            }
        }
        
        // Fallback: create simple map
        createSimpleMap();
    }
    
    private void createSimpleMap() {
        grid = new char[height][width];
        
        // Fill with walls
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                grid[i][j] = WALL;
            }
        }
        
        // Create open area
        for (int i = 2; i < height - 2; i++) {
            for (int j = 2; j < width - 2; j++) {
                grid[i][j] = EMPTY;
            }
        }
        
        playerPos = new Point(3, 3);
        boxes = new HashSet<>();
        boxes.add(new Point(4, 4));
        boxes.add(new Point(5, 4));
        
        targets = new HashSet<>();
        targets.add(new Point(width - 3, height - 3));
        targets.add(new Point(width - 4, height - 3));
        
        numBoxes = boxes.size();
        updateGrid();
    }
    
    private boolean isValidMap() {
        Set<Point> reachable = getReachablePositions(playerPos);
        
        for (Point box : boxes) {
            if (!reachable.contains(box)) return false;
        }
        for (Point target : targets) {
            if (!reachable.contains(target)) return false;
        }
        
        return true;
    }
    
    private Set<Point> getReachablePositions(Point start) {
        Set<Point> visited = new HashSet<>();
        Queue<Point> queue = new LinkedList<>();
        queue.add(start);
        visited.add(start);
        
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        
        while (!queue.isEmpty()) {
            Point p = queue.poll();
            
            for (int[] dir : dirs) {
                Point next = new Point(p.x + dir[1], p.y + dir[0]);
                
                if (!visited.contains(next) &&
                    next.y >= 0 && next.y < height &&
                    next.x >= 0 && next.x < width &&
                    grid[next.y][next.x] != WALL &&
                    !boxes.contains(next)) {
                    visited.add(next);
                    queue.add(next);
                }
            }
        }
        
        return visited;
    }
    
    private void updateGrid() {
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                if (grid[i][j] != WALL) {
                    grid[i][j] = EMPTY;
                }
            }
        }
        
        for (Point target : targets) {
            grid[target.y][target.x] = TARGET;
        }
        
        for (Point box : boxes) {
            if (targets.contains(box)) {
                grid[box.y][box.x] = BOX_ON_TARGET;
            } else {
                grid[box.y][box.x] = BOX;
            }
        }
        
        if (targets.contains(playerPos)) {
            grid[playerPos.y][playerPos.x] = PLAYER_ON_TARGET;
        } else {
            grid[playerPos.y][playerPos.x] = PLAYER;
        }
    }
    
    public boolean move(int dy, int dx) {
        // Save state for undo
        history.push(new GameState(playerPos, new HashSet<>(boxes), moves));
        
        int newY = playerPos.y + dy;
        int newX = playerPos.x + dx;
        
        // Check boundaries
        if (newY < 0 || newY >= height || newX < 0 || newX >= width) {
            history.pop();
            return false;
        }
        
        // Check wall
        if (grid[newY][newX] == WALL) {
            history.pop();
            return false;
        }
        
        Point newPos = new Point(newX, newY);
        
        // Check if there's a box
        if (boxes.contains(newPos)) {
            int boxNewY = newY + dy;
            int boxNewX = newX + dx;
            Point boxNewPos = new Point(boxNewX, boxNewY);
            
            // Check if box can be pushed
            if (boxNewY < 0 || boxNewY >= height || boxNewX < 0 || boxNewX >= width) {
                history.pop();
                return false;
            }
            
            if (grid[boxNewY][boxNewX] == WALL || boxes.contains(boxNewPos)) {
                history.pop();
                return false;
            }
            
            // Push the box
            boxes.remove(newPos);
            boxes.add(boxNewPos);
        }
        
        // Move player
        playerPos = newPos;
        moves++;
        updateGrid();
        return true;
    }
    
    public boolean undo() {
        if (!history.isEmpty()) {
            GameState state = history.pop();
            playerPos = state.playerPos;
            boxes = state.boxes;
            moves = state.moves;
            updateGrid();
            return true;
        }
        return false;
    }
    
    public boolean isWon() {
        return boxes.equals(targets);
    }
    
    public String getDisplayString() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("\nMoves: %d | Difficulty: %s\n", moves, difficulty.toUpperCase()));
        sb.append("=".repeat(width + 2)).append("\n");
        
        for (char[] row : grid) {
            sb.append(row).append("\n");
        }
        
        sb.append("=".repeat(width + 2)).append("\n");
        sb.append("\nControls: WASD to move, U to undo, R to restart, Q to quit\n");
        
        int boxesOnTarget = 0;
        for (Point box : boxes) {
            if (targets.contains(box)) boxesOnTarget++;
        }
        sb.append(String.format("Boxes on targets: %d/%d\n", boxesOnTarget, numBoxes));
        
        return sb.toString();
    }
    
    public char[][] getGrid() { return grid; }
    public int getMoves() { return moves; }
    public String getDifficulty() { return difficulty; }
    public int getBoxesOnTargets() {
        int count = 0;
        for (Point box : boxes) {
            if (targets.contains(box)) count++;
        }
        return count;
    }
    public int getNumBoxes() { return numBoxes; }
    
    // Helper classes
    private static class DifficultySettings {
        int boxes;
        double wallDensity;
        
        DifficultySettings(int boxes, double wallDensity) {
            this.boxes = boxes;
            this.wallDensity = wallDensity;
        }
    }
    
    private static class GameState {
        Point playerPos;
        Set<Point> boxes;
        int moves;
        
        GameState(Point playerPos, Set<Point> boxes, int moves) {
            this.playerPos = new Point(playerPos);
            this.boxes = boxes;
            this.moves = moves;
        }
    }
    
    // Console mode
    public static void playConsole() {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("\n=== PUSH THE BLOCK - Console Mode ===\n");
        System.out.println("Select difficulty:");
        System.out.println("1. Easy (2 boxes)");
        System.out.println("2. Medium (3 boxes)");
        System.out.println("3. Hard (4 boxes)");
        System.out.println("4. Expert (5 boxes)");
        
        System.out.print("\nEnter choice (1-4) [default: 2]: ");
        String choice = scanner.nextLine().trim();
        
        String[] difficulties = {"easy", "medium", "hard", "expert"};
        int diffIndex = choice.isEmpty() ? 1 : Math.min(Math.max(Integer.parseInt(choice) - 1, 0), 3);
        String difficulty = difficulties[diffIndex];
        
        PushBlockGame game = new PushBlockGame(difficulty, 10, 8);
        
        while (true) {
            clearScreen();
            System.out.println(game.getDisplayString());
            
            if (game.isWon()) {
                System.out.printf("\n🎉 CONGRATULATIONS! You won in %d moves! 🎉\n\n", game.getMoves());
                System.out.print("Play again? (y/n): ");
                String playAgain = scanner.nextLine().trim().toLowerCase();
                
                if (playAgain.equals("y")) {
                    game = new PushBlockGame(difficulty, 10, 8);
                } else {
                    break;
                }
            }
            
            System.out.print("Your move: ");
            String move = scanner.nextLine().trim().toLowerCase();
            
            if (move.equals("q") || move.equals("quit") || move.equals("exit")) {
                System.out.println("Thanks for playing!");
                break;
            } else if (move.equals("r") || move.equals("restart")) {
                game = new PushBlockGame(difficulty, 10, 8);
            } else if (move.equals("u") || move.equals("undo")) {
                game.undo();
            } else if (move.equals("w")) {
                game.move(-1, 0);
            } else if (move.equals("s")) {
                game.move(1, 0);
            } else if (move.equals("a")) {
                game.move(0, -1);
            } else if (move.equals("d")) {
                game.move(0, 1);
            }
        }
        
        scanner.close();
    }
    
    private static void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }
    
    // GUI mode
    public static void playGUI() {
        SwingUtilities.invokeLater(() -> new GameGUI());
    }
    
    // Main entry point
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("\n=== PUSH THE BLOCK ===\n");
        System.out.println("Choose mode:");
        System.out.println("1. GUI (Graphical)");
        System.out.println("2. Console");
        
        System.out.print("\nEnter choice (1-2) [default: 1]: ");
        String choice = scanner.nextLine().trim();
        
        scanner.close();
        
        if (choice.equals("2")) {
            playConsole();
        } else {
            playGUI();
        }
    }
}

// GUI Implementation
class GameGUI extends JFrame {
    private PushBlockGame game;
    private GamePanel gamePanel;
    private JLabel movesLabel;
    private JLabel statusLabel;
    private String currentDifficulty;
    private static final int CELL_SIZE = 40;
    
    public GameGUI() {
        setTitle("Push the Block");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);
        
        showDifficultyMenu();
        
        setLocationRelativeTo(null);
        setVisible(true);
    }
    
    private void showDifficultyMenu() {
        getContentPane().removeAll();
        
        JPanel menuPanel = new JPanel();
        menuPanel.setLayout(new BoxLayout(menuPanel, BoxLayout.Y_AXIS));
        menuPanel.setBackground(new Color(44, 62, 80));
        menuPanel.setBorder(BorderFactory.createEmptyBorder(30, 30, 30, 30));
        
        JLabel titleLabel = new JLabel("PUSH THE BLOCK");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 28));
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        menuPanel.add(titleLabel);
        menuPanel.add(Box.createVerticalStrut(30));
        
        JLabel selectLabel = new JLabel("Select Difficulty:");
        selectLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        selectLabel.setForeground(Color.WHITE);
        selectLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        menuPanel.add(selectLabel);
        menuPanel.add(Box.createVerticalStrut(20));
        
        String[][] difficulties = {
            {"Easy (2 boxes)", "easy"},
            {"Medium (3 boxes)", "medium"},
            {"Hard (4 boxes)", "hard"},
            {"Expert (5 boxes)", "expert"}
        };
        
        for (String[] diff : difficulties) {
            JButton button = createMenuButton(diff[0]);
            button.addActionListener(e -> startGame(diff[1]));
            button.setAlignmentX(Component.CENTER_ALIGNMENT);
            menuPanel.add(button);
            menuPanel.add(Box.createVerticalStrut(10));
        }
        
        add(menuPanel);
        pack();
    }
    
    private JButton createMenuButton(String text) {
        JButton button = new JButton(text);
        button.setFont(new Font("Arial", Font.PLAIN, 14));
        button.setBackground(new Color(52, 152, 219));
        button.setForeground(Color.WHITE);
        button.setFocusPainted(false);
        button.setBorderPainted(false);
        button.setPreferredSize(new Dimension(200, 40));
        button.setMaximumSize(new Dimension(200, 40));
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return button;
    }
    
    private void startGame(String difficulty) {
        currentDifficulty = difficulty;
        game = new PushBlockGame(difficulty, 10, 8);
        
        getContentPane().removeAll();
        setLayout(new BorderLayout());
        
        // Info panel
        JPanel infoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        infoPanel.setBackground(new Color(52, 73, 94));
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        movesLabel = new JLabel("Moves: 0");
        movesLabel.setFont(new Font("Arial", Font.BOLD, 14));
        movesLabel.setForeground(Color.WHITE);
        infoPanel.add(movesLabel);
        
        infoPanel.add(Box.createHorizontalStrut(20));
        
        statusLabel = new JLabel("Difficulty: " + difficulty.toUpperCase());
        statusLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        statusLabel.setForeground(Color.WHITE);
        infoPanel.add(statusLabel);
        
        add(infoPanel, BorderLayout.NORTH);
        
        // Game panel
        gamePanel = new GamePanel(game, CELL_SIZE);
        add(gamePanel, BorderLayout.CENTER);
        
        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(new Color(52, 73, 94));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        JButton undoBtn = createGameButton("Undo (U)", new Color(231, 76, 60));
        undoBtn.addActionListener(e -> undo());
        buttonPanel.add(undoBtn);
        
        JButton restartBtn = createGameButton("Restart (R)", new Color(243, 156, 18));
        restartBtn.addActionListener(e -> startGame(currentDifficulty));
        buttonPanel.add(restartBtn);
        
        JButton newGameBtn = createGameButton("New Game (N)", new Color(52, 152, 219));
        newGameBtn.addActionListener(e -> showDifficultyMenu());
        buttonPanel.add(newGameBtn);
        
        add(buttonPanel, BorderLayout.SOUTH);
        
        // Key bindings
        setupKeyBindings();
        
        pack();
        updateDisplay();
    }
    
    private JButton createGameButton(String text, Color color) {
        JButton button = new JButton(text);
        button.setFont(new Font("Arial", Font.PLAIN, 12));
        button.setBackground(color);
        button.setForeground(Color.WHITE);
        button.setFocusPainted(false);
        button.setBorderPainted(false);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        return button;
    }
    
    private void setupKeyBindings() {
        JPanel contentPane = (JPanel) getContentPane();
        contentPane.setFocusable(true);
        contentPane.requestFocusInWindow();
        
        InputMap inputMap = contentPane.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW);
        ActionMap actionMap = contentPane.getActionMap();
        
        // Arrow keys
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_UP, 0), "moveUp");
        actionMap.put("moveUp", new MoveAction(-1, 0));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_DOWN, 0), "moveDown");
        actionMap.put("moveDown", new MoveAction(1, 0));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_LEFT, 0), "moveLeft");
        actionMap.put("moveLeft", new MoveAction(0, -1));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_RIGHT, 0), "moveRight");
        actionMap.put("moveRight", new MoveAction(0, 1));
        
        // WASD keys
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_W, 0), "moveUp2");
        actionMap.put("moveUp2", new MoveAction(-1, 0));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_S, 0), "moveDown2");
        actionMap.put("moveDown2", new MoveAction(1, 0));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_A, 0), "moveLeft2");
        actionMap.put("moveLeft2", new MoveAction(0, -1));
        
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_D, 0), "moveRight2");
        actionMap.put("moveRight2", new MoveAction(0, 1));
        
        // Undo
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_U, 0), "undo");
        actionMap.put("undo", new AbstractAction() {
            public void actionPerformed(ActionEvent e) {
                undo();
            }
        });
        
        // Restart
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_R, 0), "restart");
        actionMap.put("restart", new AbstractAction() {
            public void actionPerformed(ActionEvent e) {
                startGame(currentDifficulty);
            }
        });
        
        // New game
        inputMap.put(KeyStroke.getKeyStroke(KeyEvent.VK_N, 0), "newGame");
        actionMap.put("newGame", new AbstractAction() {
            public void actionPerformed(ActionEvent e) {
                showDifficultyMenu();
            }
        });
    }
    
    private class MoveAction extends AbstractAction {
        private int dy, dx;
        
        MoveAction(int dy, int dx) {
            this.dy = dy;
            this.dx = dx;
        }
        
        public void actionPerformed(ActionEvent e) {
            if (game.move(dy, dx)) {
                updateDisplay();
                
                if (game.isWon()) {
                    JOptionPane.showMessageDialog(GameGUI.this,
                        "Congratulations! You won in " + game.getMoves() + " moves!",
                        "Victory!", JOptionPane.INFORMATION_MESSAGE);
                }
            }
        }
    }
    
    private void undo() {
        if (game.undo()) {
            updateDisplay();
        }
    }
    
    private void updateDisplay() {
        movesLabel.setText("Moves: " + game.getMoves());
        statusLabel.setText(String.format("Boxes: %d/%d", 
            game.getBoxesOnTargets(), game.getNumBoxes()));
        gamePanel.repaint();
    }
}

class GamePanel extends JPanel {
    private PushBlockGame game;
    private int cellSize;
    
    public GamePanel(PushBlockGame game, int cellSize) {
        this.game = game;
        this.cellSize = cellSize;
        
        int width = game.getGrid()[0].length * cellSize;
        int height = game.getGrid().length * cellSize;
        setPreferredSize(new Dimension(width, height));
        setBackground(new Color(26, 26, 26));
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        char[][] grid = game.getGrid();
        
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                int x = j * cellSize;
                int y = i * cellSize;
                
                char cell = grid[i][j];
                
                // Draw background
                if (cell == '.' || cell == '+') {
                    g2d.setColor(new Color(243, 156, 18));
                } else {
                    g2d.setColor(new Color(44, 62, 80));
                }
                g2d.fillRect(x, y, cellSize, cellSize);
                
                // Draw grid lines
                g2d.setColor(new Color(52, 73, 94));
                g2d.drawRect(x, y, cellSize, cellSize);
                
                // Draw entity
                if (cell == '#') {
                    g2d.setColor(new Color(127, 140, 141));
                    g2d.fillRect(x + 2, y + 2, cellSize - 4, cellSize - 4);
                } else if (cell == '$' || cell == '*') {
                    Color boxColor = (cell == '*') ? new Color(39, 174, 96) : new Color(192, 57, 43);
                    g2d.setColor(boxColor);
                    g2d.fillRect(x + 5, y + 5, cellSize - 10, cellSize - 10);
                    g2d.setColor(Color.WHITE);
                    g2d.setStroke(new BasicStroke(2));
                    g2d.drawRect(x + 5, y + 5, cellSize - 10, cellSize - 10);
                } else if (cell == '@' || cell == '+') {
                    g2d.setColor(new Color(52, 152, 219));
                    g2d.fillOval(x + 5, y + 5, cellSize - 10, cellSize - 10);
                    g2d.setColor(Color.WHITE);
                    g2d.setStroke(new BasicStroke(2));
                    g2d.drawOval(x + 5, y + 5, cellSize - 10, cellSize - 10);
                }
            }
        }
    }
}
