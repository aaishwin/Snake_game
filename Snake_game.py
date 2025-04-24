# Snake_game.py
import random
import tkinter as tk

# === Constants ===
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 250            # milliseconds between moves
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#FF0000"
FOOD_COLOR = "#00FF00"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        # Initialize snake body coordinates and canvas squares
        self.body_positions = [(0, 0)] * BODY_PARTS
        self.squares = []
        for x, y in self.body_positions:
            sq = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(sq)
        self.direction = "down"

    def move(self):
        head_x, head_y = self.body_positions[0]
        if self.direction == "up":
            new_head = (head_x, head_y - SPACE_SIZE)
        elif self.direction == "down":
            new_head = (head_x, head_y + SPACE_SIZE)
        elif self.direction == "left":
            new_head = (head_x - SPACE_SIZE, head_y)
        else:  # right
            new_head = (head_x + SPACE_SIZE, head_y)

        # Shift body positions
        self.body_positions = [new_head] + self.body_positions[:-1]

        # Move each square to its new position
        for pos, sq in zip(self.body_positions, self.squares):
            canvas.coords(
                sq,
                pos[0], pos[1],
                pos[0] + SPACE_SIZE, pos[1] + SPACE_SIZE
            )

class Food:
    def __init__(self):
        self.position = self.random_position()
        self.square = canvas.create_oval(
            self.position[0], self.position[1],
            self.position[0] + SPACE_SIZE, self.position[1] + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

    def random_position(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        return (x, y)

    def refresh(self):
        self.position = self.random_position()
        canvas.coords(
            self.square,
            self.position[0], self.position[1],
            self.position[0] + SPACE_SIZE, self.position[1] + SPACE_SIZE
        )

def next_turn():
    global score
    snake.move()
    head = snake.body_positions[0]

    # Check if food eaten
    if head == food.position:
        score += 1
        label.config(text=f"Score: {score}")
        # Grow snake by adding a new segment at tail
        snake.body_positions.append(snake.body_positions[-1])
        sq = canvas.create_rectangle(
            snake.body_positions[-1][0], snake.body_positions[-1][1],
            snake.body_positions[-1][0] + SPACE_SIZE, snake.body_positions[-1][1] + SPACE_SIZE,
            fill=SNAKE_COLOR, tag="snake"
        )
        snake.squares.append(sq)
        food.refresh()

    # Check for collisions with walls or self
    if (
        head[0] < 0 or head[0] >= GAME_WIDTH or
        head[1] < 0 or head[1] >= GAME_HEIGHT or
        head in snake.body_positions[1:]
    ):
        game_over()
    else:
        window.after(SPEED, next_turn)

def change_direction(new_dir):
    """Prevent reversing direction directly."""
    opposites = {"up":"down", "down":"up", "left":"right", "right":"left"}
    if new_dir != opposites.get(snake.direction):
        snake.direction = new_dir

def game_over():
    canvas.delete("all")
    canvas.create_text(
        GAME_WIDTH/2, GAME_HEIGHT/2,
        text="GAME OVER", fill="red",
        font=("Impact", 50)
    )


def restart_game():
    global snake, food, score, after_id
    if after_id:
        window.after_cancel(after_id)
    canvas.delete("all")
    score = 0
    label.config(text=f"Score: {score}")
    snake = Snake()
    food = Food()
    after_id = window.after(SPEED, next_turn)


# === Setup Window ===
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
label = tk.Label(
    window,
    text=f"Score: {score}",
    font=("Impact", 40),
    fg="white",
    bg=BACKGROUND_COLOR
)
label.pack(side="top", fill="x")

canvas = tk.Canvas(
    window,
    bg=BACKGROUND_COLOR,
    height=GAME_HEIGHT,
    width=GAME_WIDTH
)
canvas.pack()

# Instantiate game objects
snake = Snake()
food = Food()

# Key bindings
window.bind("<Up>",    lambda e: change_direction("up"))
window.bind("<Down>",  lambda e: change_direction("down"))
window.bind("<Left>",  lambda e: change_direction("left"))
window.bind("<Right>", lambda e: change_direction("right"))

# Start the game loop
window.after(SPEED, next_turn)
window.mainloop()
