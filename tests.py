"""Test file"""
import random
import os
import unittest
import pygame
from pygame import Vector2
from game import Game
from utilities import load_high_scores, save_high_scores
from entities import Snake, Food, Obstacle


class TestSnakeGame(unittest.TestCase):
    """Test SnakeGame"""

    def setUp(self):
        """Set up game"""
        pygame.init()
        self.game = Game()
        self.game.snake = Snake()
        self.game.food = Food()

    def tearDown(self):
        """Tear down game"""
        pygame.quit()
        if os.path.exists('high_scores.txt'):
            os.remove('high_scores.txt')

    def update_score(self, new_score):
        """Update score function we will check"""
        high_scores = load_high_scores()
        high_scores.append(new_score)
        high_scores = sorted(high_scores, reverse=True)[:5]
        save_high_scores(high_scores)

    def test_check_collision_with_food(self):
        """Check collision with food"""
        self.game.snake.body = [Vector2(5, 5)]
        self.game.food.pos = Vector2(5, 5)
        initial_length = len(self.game.snake.body)
        self.game.check_collision()
        self.game.snake.move_snake()
        self.assertEqual(len(self.game.snake.body), initial_length + 1)
        self.assertEqual(self.game.score, 1)

    def test_check_collision_with_self(self):
        """Check collision with itself"""
        self.game.snake.body = [Vector2(5, 5), Vector2(5, 4), Vector2(5, 3), Vector2(5, 5)]
        self.game.check_fail()
        self.assertTrue(self.game.game_over)

    def test_check_collision_with_obstacle(self):
        """Check collision with obstacles"""
        self.game.snake.body = [Vector2(5, 5)]
        obstacle = Obstacle(self.game)
        obstacle.positions = [Vector2(5, 5)]
        self.game.obstacles = [obstacle]
        self.game.check_fail()
        self.assertTrue(self.game.game_over)

    def test_food_randomize(self):
        """Ensure food does not spawn on the snake"""
        self.game.snake.body = [Vector2(x, 0) for x in range(10)]
        self.game.food.randomize(self.game.snake.body, [])
        self.assertNotIn(self.game.food.pos, self.game.snake.body)

    def test_food_randomize_with_obstacles(self):
        """Ensure food does not spawn on obstacles"""
        self.game.snake.body = [Vector2(0, 0)]
        obstacles = [Obstacle(self.game) for _ in range(10)]
        for obstacle in obstacles:
            obstacle.positions = [Vector2(random.randint(0, 19), random.randint(0, 19))]
        self.game.food.randomize(self.game.snake.body, obstacles)
        for obstacle in obstacles:
            self.assertNotIn(self.game.food.pos, obstacle.positions)

    def test_load_high_scores_no_file(self):
        """Test loading high scores when the file does not exist"""
        if os.path.exists('high_scores.txt'):
            os.remove('high_scores.txt')
        self.assertEqual(load_high_scores(), [])

    def test_save_high_scores(self):
        """Test saving high scores to a file"""
        high_scores = [300, 100, 200]
        save_high_scores(high_scores)
        self.assertEqual(load_high_scores(), [300, 200, 100])

    def test_update_high_scores_new_high(self):
        """Test updating high scores with a new high score"""
        save_high_scores([100, 200])
        self.update_score(300)
        self.assertEqual(load_high_scores(), [300, 200, 100])

    def test_update_high_scores_no_new_high(self):
        """Test updating high scores without a new high score"""
        save_high_scores([100, 200, 300])
        self.update_score(150)
        self.assertEqual(load_high_scores(), [300, 200, 150, 100])


if __name__ == '__main__':
    unittest.main()
