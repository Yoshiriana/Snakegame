import pygame
import random
import sys

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)  # Dark blue color for the "SNAKE GAME" text
RED = (255, 0, 0)
PURPLE = (160, 32, 240)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

FOOD_COLORS = [RED, GREEN, BLUE]  # Now fixed 3 colors for the food
SNAKE_COLORS = [GREEN, RED, PURPLE, BLUE]
color_index = 0

# Load the background image
background_image = pygame.image.load("iceberg.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Resize to fit screen

# Clock
clock = pygame.time.Clock()
SPEED = 6  # Set slower speed initially (lower number = slower)

# Fonts
font_big = pygame.font.SysFont("arial", 40)
font_small = pygame.font.SysFont("arial", 25)

# Snake settings
BLOCK = 20  # Snake body part size
RADIUS = BLOCK // 2  # Rounded body parts (using circles)
SEGMENT_MARGIN = 2  # Small margin between segments to enhance the visual effect

# Button positions
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50


def draw_text(text, font, color, x, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (x, y))


def draw_button(text, x, y, width, height, color, text_color):
    # Draw the button with a white border and the background color
    pygame.draw.rect(screen, WHITE, (x - 5, y - 5, width + 10, height + 10))  # White border
    pygame.draw.rect(screen, color, (x, y, width, height))  # Button background
    
    # Render text in the center of the button
    txt = font_small.render(text, True, text_color)
    text_rect = txt.get_rect(center=(x + width // 2, y + height // 2))  # Center the text
    screen.blit(txt, text_rect)  # Draw the text on the screen


def button_click(mouse_x, mouse_y, x, y, width, height):
    if x < mouse_x < x + width and y < mouse_y < y + height:
        return True
    return False


def countdown():
    global SPEED
    countdown_font = pygame.font.SysFont("arial", 100)

    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_text(str(i), countdown_font, WHITE, WIDTH // 2 - 50, HEIGHT // 2 - 50)
        pygame.display.update()
        pygame.time.delay(1000)

    # Start the game with a slower initial speed
    SPEED = 8  # Slightly faster than the initial value for a more natural speed


def home_screen():
    global color_index
    while True:
        # Blit the background image
        screen.blit(background_image, (0, 0))

        # Draw "SNAKE GAME" in dark blue
        draw_text("SNAKE GAME", font_big, DARK_BLUE, 190, 100)

        # Draw Home Screen Buttons (black background, white text)
        draw_button("Enter - Start Game", 175, 220, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("Customize", 175, 280, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("ESC - Quit", 175, 340, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)

        # Draw current snake color on home screen
        pygame.draw.rect(screen, SNAKE_COLORS[color_index], (260, 400, 80, 20))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Start Game Button
                if button_click(mouse_x, mouse_y, 175, 220, BUTTON_WIDTH, BUTTON_HEIGHT):
                    countdown()
                    game_loop()

                # Customize Button
                if button_click(mouse_x, mouse_y, 175, 280, BUTTON_WIDTH, BUTTON_HEIGHT):
                    color_index = (color_index + 1) % len(SNAKE_COLORS)

                # Quit Game Button
                if button_click(mouse_x, mouse_y, 175, 340, BUTTON_WIDTH, BUTTON_HEIGHT):
                    pygame.quit()
                    sys.exit()


def game_loop():
    snake_head_color = BLACK  # The head color is always black
    snake_tail_color = SNAKE_COLORS[color_index]  # The tail color is selected by the player
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = BLOCK, 0

    snake = [(x, y)]  # Initialize the snake with the head
    length = 1

    # Food positions are now fixed with specific colors
    food_positions = [(100, 100), (300, 300), (500, 500)]  # Fixed positions for food
    food_colors = [RED, GREEN, BLUE]  # Each food piece has a specific color

    score = 0

    running = True
    while running:
        # Blit the background image
        screen.blit(background_image, (0, 0))  # Draw background for each frame
        clock.tick(SPEED)  # Use the adjusted speed here

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Simple movement zones based on click positions
                if 0 <= mouse_x < WIDTH // 2:
                    if 0 <= mouse_y < HEIGHT // 2:  # Top left: Move Up
                        dx, dy = 0, -BLOCK
                    elif HEIGHT // 2 <= mouse_y < HEIGHT:  # Bottom left: Move Down
                        dx, dy = 0, BLOCK
                if WIDTH // 2 <= mouse_x < WIDTH:  # Right half for left/right movement
                    if 0 <= mouse_y < HEIGHT // 2:  # Top right: Move Left
                        dx, dy = -BLOCK, 0
                    elif HEIGHT // 2 <= mouse_y < HEIGHT:  # Bottom right: Move Right
                        dx, dy = BLOCK, 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -BLOCK
                if event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, BLOCK
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -BLOCK, 0
                if event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = BLOCK, 0

        x += dx
        y += dy
        snake.insert(0, (x, y))  # Insert the new head in front

        if len(snake) > length:
            snake.pop()  # Remove the last segment (tail)

        # Collision with wall or self
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or (x, y) in snake[1:]:
            game_over(score)
            return

        # Eat food
        for i, food_pos in enumerate(food_positions):
            food_x, food_y = food_pos
            if x == food_x and y == food_y:
                food_positions[i] = (random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK))
                length += 1
                score += 1

        # Draw food as squares with specific colors
        for i, food_pos in enumerate(food_positions):
            food_x, food_y = food_pos
            pygame.draw.rect(screen, food_colors[i], (food_x, food_y, BLOCK, BLOCK))  # Drawing colored squares

        # Draw snake as a series of circles (rounded body parts)
        for i, part in enumerate(snake):
            if i == 0:  # Draw the head (black)
                pygame.draw.circle(screen, snake_head_color, (part[0] + RADIUS, part[1] + RADIUS), RADIUS)
            else:  # Draw the tail and body (custom color)
                pygame.draw.circle(screen, snake_tail_color, (part[0] + RADIUS, part[1] + RADIUS), RADIUS)

        draw_text(f"Score: {score}", font_small, WHITE, 10, 10)

        pygame.display.update()


def game_over(score):
    while True:
        # Blit the background image
        screen.blit(background_image, (0, 0))

        draw_text("GAME OVER", font_big, RED, 200, 180)
        draw_text(f"Score: {score}", font_small, WHITE, 250, 240)

        # Game over buttons
        draw_button("Try Again", 175, 300, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)
        draw_button("Home", 175, 360, BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Try Again Button
                if button_click(mouse_x, mouse_y, 175, 300, BUTTON_WIDTH, BUTTON_HEIGHT):
                    countdown()
                    game_loop()

                # Home Button
                if button_click(mouse_x, mouse_y, 175, 360, BUTTON_WIDTH, BUTTON_HEIGHT):
                    return


home_screen()
