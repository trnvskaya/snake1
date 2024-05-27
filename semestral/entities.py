"""Module with entities"""
import random
import pygame
from pygame import Vector2
from constants import CELL_NUMBER, CELL_SIZE

class Snake:
    """Class for defining the snake"""
    def __init__(self):
        """Initialize the snake"""
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.next_direction = self.direction
        self.new_block = False
        self.color = (0, 0, 255)

    def draw_snake(self, screen, color):
        """Draw the snake"""
        for block in self.body:
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, block_rect)

    def move_snake(self):
        """Move the snake"""
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        """Add a block to the snake"""
        self.new_block = True


class Food:
    """Class for defining the food"""
    def __init__(self):
        """Initialize the food"""
        self.pos = Vector2(0, 0)
        self.x = None
        self.y = None
        self.points = 1
        self.food_image = pygame.image.load('Graphics/burger (2).png').convert_alpha()

    def draw_food(self, screen):
        """Draw the food"""
        food_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(self.food_image, food_rect)

    def randomize(self, snake_body, obstacles):
        """Randomize the food position"""
        while True:
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
            if self.is_valid_position(self.pos, snake_body, obstacles):
                break

    def is_valid_position(self, pos, snake_body, obstacles):
        """Check if the position is valid"""
        if pos in snake_body:
            return False
        for obstacle in obstacles:
            if pos in obstacle.positions:
                return False
        return True

    def get_points(self):
        """Get the points of the food"""
        return self.points


class Obstacle:
    """Class for defining the obstacle"""
    def __init__(self, game):
        """Initialize the obstacle"""
        self.game = game
        self.positions = []

    def randomize(self):
        """Randomize the obstacle"""
        length = random.choice([2, 3])
        while len(self.positions) < length:
            if len(self.positions) == 0:
                new_pos = Vector2(random.randint(0, CELL_NUMBER - 1), random.randint(0, CELL_NUMBER - 1))
            else:
                direction = random.choice([Vector2(1, 0), Vector2(0, 1)])
                new_pos = self.positions[-1] + direction

            if self.is_valid_position(new_pos):
                self.positions.append(new_pos)
            else:
                self.positions = []
                length = random.choice([2, 3])

    def is_valid_position(self, pos):
        """Check if the position is valid"""
        initial_snake_pos = self.game.snake.body[0]
        if not (0 <= pos.x < CELL_NUMBER and 0 <= pos.y < CELL_NUMBER):
            return False
        if pos in self.game.snake.body or pos == self.game.food.pos:
            return False
        if pos.distance_to(initial_snake_pos) <= 3:
            return False
        for other in self.game.obstacles:
            if pos in other.positions and other != self:
                return False
        return True

    def draw_obstacle(self, screen):
        """Draw the obstacle"""
        for pos in self.positions:
            obstacle_rect = pygame.Rect(pos.x * CELL_SIZE, pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (72, 60, 50), obstacle_rect)
