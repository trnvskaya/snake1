# Snake Game

This project is a classic Snake game implemented in Python using the Pygame library. The game features a snake that the player controls to eat food and grow longer while avoiding obstacles and its own tail. The game tracks high scores and allows players to compete for the highest score.

## Features

- Control the snake to eat food and grow longer.
- Avoid running into obstacles or the snake's own tail.
- Dynamic generation of obstacles and food.
- Bonus food for gaining higher score.
- Two levels of difficulty you may choose on the start screen.
- High score tracking.
- Adjustable game settings.

## Dependencies

- Python 3.x
- Pygame

## Installation

To run the game, you need to download the libraries using the following command: \
`pip install Pygame`

## Running the Game

Then simply run the code in the `main.py` file from the project directory

## Controls

The controls are very simple:

Left and Right Arrows: Move the snake left and right.
Up Arrow: Move the snake up.
Down Arrow: Move the snake down

## Implementation details

The game is implemented using the Pygame library. The main components include:

Snake: Class for defining the snake.
Food: Class for defining the food.
Obstacle: Class for defining the obstacles.
High Score Management: High scores are saved in the high_scores.txt file in the project's root directory.
Obstacles are not generated within a 3-block radius of the snake's initial spawn position to ensure the player has enough space to start the game.

## Tests

(How this works in terminal for me)
`python -m unittest tests.py`

