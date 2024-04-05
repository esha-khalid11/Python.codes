import pygame
import random
import os  # Import the os module to check file existence

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 149, 237)  # Light blue color

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
background_color = LIGHT_BLUE

# Game Title
pygame.display.set_caption("SnakeGame")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 35)

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(LIGHT_BLUE)
        text_screen("Welcome to Snake game", BLACK, 250, 250)  # Center-align vertically
        text_screen("Press space bar to start", BLACK, 250, 300)  # Center-align vertically
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
                
        pygame.display.update()
        clock.tick(60)
def text_screen(text, color, x, y, align="left"):
    lines = text.split("\n")
    max_width = max([font.size(line)[0] for line in lines])
    total_height = sum([font.size(line)[1] for line in lines])
    
    y_pos = y
    for line in lines:
        if align == "left":
            x_pos = x
        elif align == "center":
            x_pos = x + (max_width - font.size(line)[0]) // 2
        else:
            x_pos = x + (max_width - font.size(line)[0])
        
        screen_text = font.render(line, True, color)
        gameWindow.blit(screen_text, (x_pos, y_pos))
        y_pos += font.size(line)[1]      
        

def plot_snake(gameWindow, color, snk_list, snake_size):
    for segment in snk_list:
        pygame.draw.circle(gameWindow, color, (segment[0], segment[1]), snake_size // 2)  # Draw circles for snake

# Game Loop
def gameloop():
    # Check if the highscore.txt file exists, if not, create it
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                highscore = f.write(str(highscore))

            gameWindow.fill(WHITE)
            text_screen("Game Over! Press Enter To Continue", RED, 150,250)  # Center-align text

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                        
                    if event.key == pygame.K_g:
                        background_color = GREEN

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                        
                    if event.key == pygame.K_w:
                        score += 20

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 20 and abs(snake_y - food_y) < 20:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5
                
                if score > int(highscore):
                    highscore = score

            gameWindow.fill(GREEN)
            text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), RED, 5, 5)
            pygame.draw.circle(gameWindow, RED, (food_x + snake_size // 2, food_y + snake_size // 2), snake_size // 2)  # Draw circle for food

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                
            plot_snake(gameWindow, BLACK, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
