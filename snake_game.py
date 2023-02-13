# Import the Turtle Graphics and random modules
import turtle
import random
from tkinter import PhotoImage
from turtle import Turtle, Screen, Shape

# Define program constants
WIDTH = 500
HEIGHT = 500
DELAY = 100  # Milliseconds
FOOD_SIZE = 10

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")


def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":  # No self-collision simply by pressing wrong key.
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"


def game_loop():
    stamper.clearstamps()  # Remove existing stamps made by stamper.

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        snakeStops()
    else:
        # Add new head to snake body.
        snake.append(new_head)

        # Check food collision
        if not food_collision():
            snake.pop(0)  # Keep the snake the same length unless fed.

        # Draw snake for the first time.
        count = 0
        for segment in snake:
            if count % 2 == 0:
                stamper.color('#04de87')
            else:
                stamper.color('#0288d6')
            stamper.goto(segment[0], segment[1])
            stamper.stamp()
            count += 1

        # Refresh screen
        screen.title(f"Snake Game. Score: {score}")
        screen.update()

        # Rinse and repeat
        turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, score, DELAY
    if get_distance(snake[-1], food_pos) < 20:
        score += 1  # score = score + 1
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        DELAY = DELAY - 2
        return True
    return False


def get_random_food_pos():
    x = random.randint(- WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(- HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras' Theorem
    return distance


def snakeStops():
    global snake, score, food_pos, snake_direction
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    score = 0
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    screen.title("Press space to start")
    count = 0
    for segment in snake:
        if count % 2 == 0:
            stamper.color('#04de87')
        else:
            stamper.color('#0288d6')
        stamper.goto(segment[0], segment[1])
        stamper.stamp()
        count += 1
    screen.update()

def reset():
    global  snake, score, snake_direction, food_pos, DELAY
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    score = 0
    snake_direction = "up"
    DELAY = 100
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()



# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)  # Set the dimensions of the Turtle Graphics window.
screen.title("Press space to start")
screen.bgcolor("#1b1d21")
screen.tracer(0)  # Turn off automatic animation.
larger = PhotoImage(file="apple_04.gif").zoom(1, 1)
screen.addshape("larger", Shape("image", larger))

# Event handlers
screen.listen()
bind_direction_keys()
screen.onkey(reset,'space')

# Create a turtle to do your bidding
stamper = turtle.Turtle()
stamper.shape("square")
stamper.shapesize(30 / 20)
stamper.penup()

# Food
food = turtle.Turtle('larger')
food.penup()

snakeStops()

# Finish nicely
turtle.done()
