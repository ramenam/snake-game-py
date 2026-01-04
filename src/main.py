from tkinter import *
import random
import pygame

# Game configuration constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#F2F700"
BACKGROUND_COLOR = "#000000"


# Class representing the snake in the game
class Snake:
    def __init__(self):
        # Initialize the snake's body size
        self.body_size = BODY_PARTS
        # List to hold the coordinates of each body part
        self.coordinates = []
        # List to hold the canvas squares representing the snake
        self.squares = []

        # Create initial body parts at (0,0)
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Draw the initial snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


# Class representing the food in the game
class Food:
    def __init__(self):
        # Generate random coordinates for the food within the game grid
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        # Draw the food on the canvas
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


# Function to handle the next turn of the game
def next_turn(snake, food):
    # Get the current head position
    x, y = snake.coordinates[0]

    # Move the head based on the current direction
    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    # Add new head position to coordinates
    snake.coordinates.insert(0, (x, y))
    # Draw the new head on the canvas
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if food is eaten
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score 
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food.__init__()
    else:   
        # Remove the tail if no food eaten
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn
        window.after(SPEED, next_turn, snake, food)


# Function to change the direction of the snake
def change_direction(new_direction):
    global direction
    # Prevent reversing into the snake's body
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


# Function to check for collisions with walls or self
def check_collisions(snake):
    x, y = snake.coordinates[0]
    # Check wall collisions
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    # Check self-collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


# Function to display game over screen
def game_over():
    canvas.delete(ALL)
    # Stop background music
    pygame.mixer.music.stop()
    # Display "GAME OVER" text
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    # Display final score
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 100,
                          font=('consolas',30), text="Final Score: {}".format(score), fill="white", tag="score")
    # Display restart instruction
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 150,
                            font=('consolas',20), text="Press 'R' to Restart", fill="white", tag="restart")
    # Bind 'R' key to restart
    canvas.bind_all('<r>', restart_game)

# Function to restart the game
def restart_game(event):
    global score, direction
    # Reset score and direction
    score = 0
    direction = 'down'
    label.config(text="Score: {}".format(score))
    canvas.delete(ALL)
    # Restart background music
    pygame.mixer.music.play(-1)
    # Create new snake and food
    snake = Snake()
    food = Food()
    # Start the game loop
    next_turn(snake, food)


# Main game window setup
# Main game window setup
window = Tk()
# Initialize pygame for audio
pygame.init()
# Load and play background music in a loop
music_file = 'snake-py-bgm.wav'
pygame.mixer.music.load(music_file) 
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

window.title("Snake Game")
window.resizable(False, False)

# Initialize score and direction
score = 0
direction = 'down'

# Create score label
label = Label(window, text="Score: {}".format(score), font=('consolas', 30))
label.pack()

# Create game canvas
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Update window to get dimensions
window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2)  )
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize snake and food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Start the Tkinter main loop
window.mainloop()
