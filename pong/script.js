const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

// Game settings
const paddleWidth = 16;
const paddleHeight = 100;
const ballSize = 16;
const playerX = 30;
const aiX = canvas.width - playerX - paddleWidth;
let playerY = canvas.height / 2 - paddleHeight / 2;
let aiY = canvas.height / 2 - paddleHeight / 2;

let ballX = canvas.width / 2 - ballSize / 2;
let ballY = canvas.height / 2 - ballSize / 2;
let ballSpeedX = 6;
let ballSpeedY = 4;

// Score (optional)
let playerScore = 0;
let aiScore = 0;

// Mouse control for player paddle
canvas.addEventListener('mousemove', function(e) {
    const rect = canvas.getBoundingClientRect();
    let mouseY = e.clientY - rect.top;
    playerY = mouseY - paddleHeight / 2;

    // Clamp paddle within canvas
    if (playerY < 0) playerY = 0;
    if (playerY + paddleHeight > canvas.height) playerY = canvas.height - paddleHeight;
});

// Game loop
function gameLoop() {
    update();
    draw();
    requestAnimationFrame(gameLoop);
}

// Update game state
function update() {
    // Move ball
    ballX += ballSpeedX;
    ballY += ballSpeedY;

    // Ball collision: Top and bottom walls
    if (ballY <= 0 || ballY + ballSize >= canvas.height) {
        ballSpeedY = -ballSpeedY;
    }

    // Ball collision: Player paddle
    if (
        ballX <= playerX + paddleWidth &&
        ballX >= playerX &&
        ballY + ballSize >= playerY &&
        ballY <= playerY + paddleHeight
    ) {
        ballSpeedX = -ballSpeedX;
        // Add a bit of "spin" based on where it hits the paddle
        let hitPos = (ballY + ballSize / 2) - (playerY + paddleHeight / 2);
        ballSpeedY += hitPos * 0.15;
    }

    // Ball collision: AI paddle
    if (
        ballX + ballSize >= aiX &&
        ballX + ballSize <= aiX + paddleWidth &&
        ballY + ballSize >= aiY &&
        ballY <= aiY + paddleHeight
    ) {
        ballSpeedX = -ballSpeedX;
        let hitPos = (ballY + ballSize / 2) - (aiY + paddleHeight / 2);
        ballSpeedY += hitPos * 0.15;
    }

    // Ball out of bounds: left or right
    if (ballX < 0) {
        aiScore++;
        resetBall();
    }
    if (ballX + ballSize > canvas.width) {
        playerScore++;
        resetBall();
    }

    // AI paddle movement (basic tracking)
    let aiCenter = aiY + paddleHeight / 2;
    if (aiCenter < ballY + ballSize / 2 - 10) {
        aiY += 5;
    } else if (aiCenter > ballY + ballSize / 2 + 10) {
        aiY -= 5;
    }

    // Clamp AI paddle within canvas
    if (aiY < 0) aiY = 0;
    if (aiY + paddleHeight > canvas.height) aiY = canvas.height - paddleHeight;
}

// Draw everything
function draw() {
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw middle line
    ctx.fillStyle = '#fff';
    ctx.globalAlpha = 0.2;
    for (let y = 10; y < canvas.height; y += 40) {
        ctx.fillRect(canvas.width / 2 - 2, y, 4, 20);
    }
    ctx.globalAlpha = 1;

    // Draw paddles
    ctx.fillStyle = '#fff';
    ctx.fillRect(playerX, playerY, paddleWidth, paddleHeight);
    ctx.fillRect(aiX, aiY, paddleWidth, paddleHeight);

    // Draw ball
    ctx.beginPath();
    ctx.arc(ballX + ballSize / 2, ballY + ballSize / 2, ballSize / 2, 0, Math.PI * 2);
    ctx.fill();

    // Draw scores
    ctx.font = "32px Arial";
    ctx.textAlign = "center";
    ctx.fillText(playerScore, canvas.width / 2 - 60, 50);
    ctx.fillText(aiScore, canvas.width / 2 + 60, 50);
}

// Reset ball after a score
function resetBall() {
    ballX = canvas.width / 2 - ballSize / 2;
    ballY = canvas.height / 2 - ballSize / 2;
    // Randomize direction
    ballSpeedX = (Math.random() > 0.5 ? 1 : -1) * 6;
    ballSpeedY = (Math.random() > 0.5 ? 1 : -1) * 4;
}

gameLoop();