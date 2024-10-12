import pygame
import threading
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PACMAN_RADIUS = 7  # Smaller Pac-Man
DOT_SIZE = 5
DOT_COLOR = (0, 0, 0)  # Black
PACMAN_COLOR = (255, 255, 0)  # Yellow
BACKGROUND_COLOR = (255, 255, 255)  # White
WALL_COLOR = (0, 0, 0)  # Black
WALL_THICKNESS = 10
pacman_speed = 1
game_over = False
game_won = False
end_point = (SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30)  # End point in bottom-right corner

# Maze represented by a 2D array
maze = [
    "111111111111111111111111",
    "100000000000000000000001",
    "101111111111011111110101",
    "100000100001000000010001",
    "111110101111011101010101",
    "100000100000000001000001",
    "101111111011111101011111",
    "100000000010000001000001",
    "111111111111011111111111",
    "100000000000000000000001",
    "111111111111111111111101",
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man Maze")

# Pac-Man's starting position
pacman_x, pacman_y = 30, 30  # Start at top-left of the maze

# Create dots scattered in the maze
dots = [(x * 25 + 12, y * 25 + 12) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == '0']

# Font for score and game over screen
font = pygame.font.SysFont(None, 36)
score = 0

# Function to draw the maze
def draw_maze():
    block_size = SCREEN_WIDTH // len(maze[0])
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '1':  # Draw walls
                pygame.draw.rect(screen, WALL_COLOR, (x * block_size, y * block_size, block_size, block_size))

# Function to display score
def display_score():
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, SCREEN_HEIGHT - 40))

# Function to display control instructions
def display_instructions():
    instruction_text = font.render("Use arrow keys to control", True, (0, 0, 0))
    screen.blit(instruction_text, (SCREEN_WIDTH - 320, SCREEN_HEIGHT - 40))

# Function to display game over screen
def game_over_screen():
    screen.fill(BACKGROUND_COLOR)
    
    # "Game Over" text
    game_over_text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    # "Restart" button
    restart_button_text = font.render("Restart", True, (255, 0, 0))
    button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.draw.rect(screen, (200, 200, 200), button_rect.inflate(20, 10))
    screen.blit(restart_button_text, button_rect)

    pygame.display.flip()

    # Wait for restart click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
                    reset_game()

# Function to display the winning screen
def game_win_screen():
    screen.fill(BACKGROUND_COLOR)
    
    # "You Win" text
    win_text = font.render("You Win!", True, (0, 0, 0))
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    
    # "Restart" button
    restart_button_text = font.render("Restart", True, (255, 0, 0))
    button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.draw.rect(screen, (200, 200, 200), button_rect.inflate(20, 10))
    screen.blit(restart_button_text, button_rect)

    pygame.display.flip()

    # Wait for restart click
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
                    reset_game()

# Function to reset the game
def reset_game():
    global pacman_x, pacman_y, dots, score, game_over, game_won
    pacman_x, pacman_y = 30, 30  # Reset Pac-Man's position
    dots = [(x * 25 + 12, y * 25 + 12) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == '0']
    score = 0
    game_over = False
    game_won = False

# Function to move Pac-Man concurrently
def move_pacman():
    global pacman_x, pacman_y
    while True:
        if not game_over and not game_won:
            keys = pygame.key.get_pressed()

            new_x, new_y = pacman_x, pacman_y
            if keys[pygame.K_LEFT]:
                new_x -= pacman_speed
            if keys[pygame.K_RIGHT]:
                new_x += pacman_speed
            if keys[pygame.K_UP]:
                new_y -= pacman_speed
            if keys[pygame.K_DOWN]:
                new_y += pacman_speed

            # Check for wall collision
            if not check_wall_collision(new_x, new_y):
                pacman_x, pacman_y = new_x, new_y

        time.sleep(0.01)  # Small delay to simulate movement speed

# Function to check for wall collision
def check_wall_collision(x, y):
    global game_over
    block_size = SCREEN_WIDTH // len(maze[0])
    grid_x = x // block_size
    grid_y = y // block_size
    if maze[grid_y][grid_x] == '1':  # If it's a wall, game over
        game_over = True
    return game_over

# Function to check for dot consumption and winning condition
def check_collision():
    global dots, score, game_won
    while True:
        if not game_over and not game_won:
            # Remove dots that Pac-Man has consumed
            new_dots = []
            for dot in dots:
                if abs(pacman_x - dot[0]) < PACMAN_RADIUS and abs(pacman_y - dot[1]) < PACMAN_RADIUS:
                    score += 1  # Increment score when a dot is eaten
                else:
                    new_dots.append(dot)
            dots = new_dots

            # Check if Pac-Man has reached the end point (bottom-right corner)
            if abs(pacman_x - end_point[0]) <= PACMAN_RADIUS and abs(pacman_y - end_point[1]) <= PACMAN_RADIUS:
                game_won = True

        time.sleep(0.1)  # Slight delay to simulate checking

# Start threads for movement and collision detection
move_thread = threading.Thread(target=move_pacman, daemon=True)
collision_thread = threading.Thread(target=check_collision, daemon=True)

move_thread.start()
collision_thread.start()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not game_won:
        # Fill the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the maze
        draw_maze()

        # Draw Pac-Man
        pygame.draw.circle(screen, PACMAN_COLOR, (pacman_x, pacman_y), PACMAN_RADIUS)

        # Draw dots
        for dot in dots:
            pygame.draw.line(screen, DOT_COLOR, dot, (dot[0], dot[1] + DOT_SIZE), 2)

        # Display score and instructions
        display_score()
        display_instructions()

        # Update the display
        pygame.display.flip()
        
        # Control frame rate
        pygame.time.Clock().tick(30)
    elif game_over:
        # Show the game over screen when Pac-Man hits a wall
        game_over_screen()
    elif game_won:
        # Show the win screen when Pac-Man reaches the end
        game_win_screen()

# Quit Pygame
pygame.quit()