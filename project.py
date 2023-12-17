import pygame
import time
import random

pygame.init()

# Set up the game window
width, height = 800, 600
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define colors
dark_black = (10, 10, 10)
red = (255, 69, 0)

# Snake and apple sizes
snake_block = 10
snake_speed = 15

# Snake function
def snake(snake_block, snake_list):
    for i, segment in enumerate(snake_list):
        # Calculate gradient color based on segment position
        gradient_color = (255, int(255 - i * (255 / len(snake_list))), 0)
        
        # Draw rectangles instead of circles
        rect_width = int(snake_block * 1.5)  # Adjust width for elongation
        rect_height = snake_block
        pygame.draw.rect(game_display, gradient_color, (int(segment[0]), int(segment[1]), rect_width, rect_height))

# Ember function for drawing food
def draw_ember(x, y, size):
    pygame.draw.circle(game_display, red, (int(x), int(y)), size)

# Obstacle function for drawing obstacles
def draw_obstacle(x, y, size):
    pygame.draw.rect(game_display, (0, 255, 0), [x, y, size, size])

# Initialize current_direction globally
current_direction = "RIGHT"

# Main game loop
def game_loop():
    global current_direction
    game_over = False
    game_close = False

    # Snake initial position
    lead_x = width / 2
    lead_y = height / 2

    # Snake initial movement
    lead_x_change = 0
    lead_y_change = 0

    # Snake body
    snake_list = []
    snake_length = 1

    # Ember position (food)
    ember_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    ember_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Obstacle positions
    num_obstacles = 10
    obstacles = [(round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
                  round(random.randrange(0, height - snake_block) / 10.0) * 10.0)
                 for _ in range(num_obstacles)]

    while not game_over:

        while game_close:
            game_display.fill(dark_black)
            font = pygame.font.SysFont(None, 50)
            text_width, text_height = font.size("You Lost! Press Q-Quit or C-Play Again")
            text_x = (width - text_width) / 2
            text_y = (height - text_height) / 2
            message = font.render("You Lost! Press Q-Quit or C-Play Again", True, red)
            game_display.blit(message, [text_x, text_y])
            snake(snake_block, snake_list)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        # Modified event handling loop
        new_direction = current_direction  # Initialize new_direction

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != "RIGHT":
                    new_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and current_direction != "LEFT":
                    new_direction = "RIGHT"
                elif event.key == pygame.K_UP and current_direction != "DOWN":
                    new_direction = "UP"
                elif event.key == pygame.K_DOWN and current_direction != "UP":
                    new_direction = "DOWN"

        # Update direction
        current_direction = new_direction

        # Update snake position
        lead_x_change, lead_y_change = 0, 0  # Reset changes at the beginning

        # Update direction
        if current_direction == "LEFT":
            lead_x_change = -snake_block
        elif current_direction == "RIGHT":
            lead_x_change = snake_block
        elif current_direction == "UP":
            lead_y_change = -snake_block
        elif current_direction == "DOWN":
            lead_y_change = snake_block

        lead_x += lead_x_change
        lead_y += lead_y_change

        # Check boundaries
        if lead_x >= width or lead_x < 0 or lead_y >= height or lead_y < 0:
            game_close = True

        # Update snake body
        snake_head = [lead_x, lead_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check if snake collides with itself or obstacles
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        for obstacle in obstacles:
            if obstacle[0] == snake_head[0] and obstacle[1] == snake_head[1]:
                game_close = True

        # Draw everything on the screen
        game_display.fill(dark_black)
        draw_ember(ember_x + snake_block // 2, ember_y + snake_block // 2, snake_block // 2)
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1], snake_block)
        snake(snake_block, snake_list)

        pygame.display.update()

        # Check if snake eats the ember
        if lead_x == ember_x and lead_y == ember_y:
            ember_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            ember_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            snake_length += 1

        # Set the game speed
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

# Start the game
game_loop()
