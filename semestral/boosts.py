"""Module with boost"""
import random
import pygame
from pygame import Vector2
from constants import CELL_SIZE, CELL_NUMBER


class Point5Apple:
    """Class with apple for 5 points"""
    def __init__(self, x, y):
        """Initialize the apple"""
        self.x = None
        self.y = None
        self.pos = Vector2(x, y)
        self.image = pygame.image.load('Graphics/burger_boost.png').convert_alpha()
        self.points = 5
        self.duration = 5000
        self.spawn_time = pygame.time.get_ticks()

    def draw_food(self, screen):
        """Draw the food"""
        food_rect = pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(self.image, food_rect)

    def randomize(self, snake_body, obstacles):
        """Randomize the food"""
        while True:
            self.x = random.randint(0, CELL_NUMBER - 1)
            self.y = random.randint(0, CELL_NUMBER - 1)
            self.pos = Vector2(self.x, self.y)
            if self.is_valid_position(self.pos, snake_body, obstacles):
                break

    def is_valid_position(self, pos, snake_body, obstacles):
        """Validate the position"""
        if pos in snake_body:
            return False
        for obstacle in obstacles:
            if pos in obstacle.positions:
                return False
        return True

    def get_points(self):
        """Get the number of points"""
        return self.points
