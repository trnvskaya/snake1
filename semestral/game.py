"""Module for game logic"""
import random
import pygame
from pygame import Vector2
from pygame.locals import QUIT, KEYDOWN, K_0, K_1, K_2, K_3, K_q, K_r, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_c, K_s
from entities import Snake, Food, Obstacle
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, CELL_NUMBER
from utilities import load_high_scores, save_high_scores
from ui import Button, Label
from boosts import Point5Apple


class Game:
    """Main game class"""
    def __init__(self):
        """Initialize game"""
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_images = [
            pygame.image.load('Graphics/background1.png').convert(),
            pygame.image.load('Graphics/background2.jpg').convert(),
            pygame.image.load('Graphics/background3.jpg').convert()
        ]
        self.current_bg = 0
        self.use_default_background = True
        self.bg_image = self.background_images[self.current_bg]
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.obstacles = [Obstacle(self) for _ in range(10)]  # Create obstacles
        for obstacle in self.obstacles:
            obstacle.randomize()
        self.food.randomize(self.snake.body, self.obstacles)
        self.play_with_obstacles = True
        self.score_font = pygame.font.Font(None, 42)
        self.high_scores = load_high_scores()
        self.game_over_sound = pygame.mixer.Sound("screamer.mp3")
        self.eat_sound = pygame.mixer.Sound("crunch.wav")
        self.poof_sound = pygame.mixer.Sound("poof.mp3")
        self.game_over = False
        self.score = 0
        self.direction_changed = False
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 150)
        self.last_eaten_time = pygame.time.get_ticks()
        self.time_limit_without_food = 10000
        self.game_start_time = 0
        self.load_music_tracks()
        self.current_track_index = 0
        pygame.mixer.music.load(self.tracks[self.current_track_index])
        pygame.mixer.music.play(-1)

    def show_start_screen(self):
        """Show start screen"""
        toggle_obstacle_button = Button(self.screen, (0, 120, 15), 250, 300, 200, 50, 'Level',
                                        (0, 0, 0))
        start_active = True
        while start_active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False
                if event.type == KEYDOWN:
                    if event.key == K_s:
                        start_active = False
                    elif event.key == K_q:
                        pygame.quit()
                        return False
                    elif event.key == K_c:
                        self.show_settings_screen()
                elif toggle_obstacle_button.is_clicked(event):
                    self.play_with_obstacles = not self.play_with_obstacles
                    toggle_obstacle_button.text = f'{"Medium" if self.play_with_obstacles else "Easy"}'

            self.screen.fill((175, 215, 70))
            start_text = "Press 'S' to Start, 'C' for menu, 'Q' to Quit"
            start_surface = self.score_font.render(start_text, True, (255, 0, 0))
            start_rect = start_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            pygame.draw.rect(self.screen, (255, 255, 255), start_rect, border_radius=10)
            self.screen.blit(start_surface, start_rect)
            toggle_obstacle_button.draw()
            pygame.display.update()

        return True

    def run(self):
        """Start the game"""
        if not self.show_start_screen():
            return
        self.game_start_time = pygame.time.get_ticks()

        while not self.game_over:
            if self.play_with_obstacles:
                if not hasattr(self, 'obstacles') or not self.obstacles:
                    self.obstacles = [Obstacle(self) for _ in range(10)]
                    for obstacle in self.obstacles:
                        obstacle.randomize()
            else:
                self.obstacles = []
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == self.timer_event:
                    self.update()
                elif event.type == KEYDOWN:
                    self.handle_keys(event.key)

            if self.play_with_obstacles:
                background_color = (220, 20, 60)
                self.snake.color = (245, 222, 179)
            else:
                background_color = (170, 215, 70)
            self.screen.fill(background_color)
            self.draw_palette()
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(60)
        self.handle_game_over()

    def update(self):
        """Update game stats"""
        if self.snake.next_direction:
            self.snake.direction = self.snake.next_direction
        self.snake.move_snake()
        self.direction_changed = False
        self.check_collision()
        self.check_fail()
        self.adjust_timer()
        if not self.game_over:
            current_time = pygame.time.get_ticks() - self.game_start_time
            time_since_last_food = current_time - self.last_eaten_time
            if self.play_with_obstacles and time_since_last_food > self.time_limit_without_food:
                self.game_over = True
        current_time = pygame.time.get_ticks()
        if isinstance(self.food, Point5Apple):
            if (current_time - self.food.spawn_time) > self.food.duration:
                self.poof_sound.play()
                self.spawn_food()

    def draw_elements(self):
        """Draw elements"""
        self.snake.draw_snake(self.screen, self.snake.color)
        self.food.draw_food(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw_obstacle(self.screen)
        self.score_draw()

    def load_music_tracks(self):
        """Load music"""
        self.tracks = ['game_music_basic.mp3', 'game_music_10.mp3', 'game_music_15.mp3', 'game_music_20.mp3', '']

    def update_music_track(self):
        """Determine the track based on score"""
        if self.score < 10:
            new_track_index = 0
        elif self.score < 20:
            new_track_index = 1
        elif self.score < 30:
            new_track_index = 2
        else:
            new_track_index = 3

        if self.current_track_index != new_track_index:
            self.current_track_index = new_track_index
            pygame.mixer.music.load(self.tracks[self.current_track_index])
            pygame.mixer.music.play(-1)

    def spawn_food(self):
        """Spawn food on the field"""
        if random.randint(0, 20) == 0:
            x = random.randint(0, CELL_NUMBER - 1)
            y = random.randint(0, CELL_NUMBER - 1)
            self.food = Point5Apple(x, y)
            self.eat_sound = pygame.mixer.Sound("magic.mp3")
        else:
            self.food = Food()
            self.food.randomize(self.snake.body, self.obstacles)
            self.eat_sound = pygame.mixer.Sound("crunch.wav")
        self.last_eaten_time = pygame.time.get_ticks() - self.game_start_time

    def change_background(self, index):
        """Change background if needed"""
        if 0 <= index < len(self.background_images):
            self.current_bg = index
            if self.background_images[index] is not None:
                scaled_image = pygame.transform.scale(self.background_images[index], (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.bg_image = scaled_image
            else:
                self.bg_image = None
            self.use_default_background = index == 0

    def draw_palette(self):
        """Draw palette if default background is used"""
        if self.use_default_background:
            if self.play_with_obstacles:
                grass_color = (165, 42, 42)
            else:
                grass_color = (160, 210, 60)
            for row in range(CELL_NUMBER):
                for col in range(CELL_NUMBER):
                    if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                        background_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(self.screen, grass_color, background_rect)
        else:
            self.screen.blit(self.bg_image, (0, 0))

    def check_collision(self):
        """Check collision with objects"""
        if self.food.pos == self.snake.body[0]:
            self.eat_sound.play()
            self.snake.add_block()
            self.score += self.food.get_points()
            self.spawn_food()
            self.last_eaten_time = pygame.time.get_ticks() - self.game_start_time
            self.update_music_track()

    def check_fail(self):
        """Check for player fail"""
        head = self.snake.body[0]
        if not 0 <= head.x < CELL_NUMBER or not 0 <= head.y < CELL_NUMBER or head in self.snake.body[1:]:
            self.update_score(self.score)
            self.game_over = True
        if self.play_with_obstacles:
            for obstacle in self.obstacles:
                if head in obstacle.positions:
                    self.update_score(self.score)
                    self.game_over = True

    def handle_keys(self, key):
        """Handle keys"""
        direction = self.snake.direction
        if not self.direction_changed:
            if key == K_UP and direction.y != 1:
                self.snake.next_direction = Vector2(0, -1)
                self.direction_changed = True
            elif key == K_DOWN and direction.y != -1:
                self.snake.next_direction = Vector2(0, 1)
                self.direction_changed = True
            elif key == K_LEFT and direction.x != 1:
                self.snake.next_direction = Vector2(-1, 0)
                self.direction_changed = True
            elif key == K_RIGHT and direction.x != -1:
                self.snake.next_direction = Vector2(1, 0)
                self.direction_changed = True

    def update_score(self, new_score):
        """Update user's score and save high scores to file"""
        self.high_scores.append(new_score)
        self.high_scores = sorted(self.high_scores, reverse=True)[:5]  # Keep only top 5 scores
        save_high_scores(self.high_scores)

    def score_draw(self):
        """Draw score"""
        score = self.score
        score_text = f"Score: {score}"
        score_surface = self.score_font.render(score_text, True, (255, 255, 255))
        score_rect = score_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(score_surface, score_rect)

    def adjust_timer(self):
        """Adjust the snake speed"""
        interval = 100 - self.score * 2
        interval = max(interval, 50)
        pygame.time.set_timer(self.timer_event, int(interval))

    def handle_game_over(self):
        """Handle game over"""
        pygame.mixer.music.stop()
        self.game_over_sound.play()
        game_over_text = "Game Over! Your final score: " + str(self.score)
        game_over_surface = self.score_font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        pygame.draw.rect(self.screen, (255, 255, 255), game_over_rect, border_radius=10)
        self.screen.blit(game_over_surface, game_over_rect)

        # High scores display
        high_score_text = "High Scores:"
        high_score_y = game_over_rect.bottom + 30
        high_score_surface = self.score_font.render(high_score_text, True, (255, 0, 0))
        high_score_rect = high_score_surface.get_rect(midtop=(game_over_rect.centerx, high_score_y))
        pygame.draw.rect(self.screen, (255, 255, 255), high_score_rect, border_radius=5)
        self.screen.blit(high_score_surface, high_score_rect)

        # Sort and limit high scores
        sorted_high_scores = sorted(self.high_scores, reverse=True)[:5]  # Sort descending and take top 5

        high_score_y += 40
        for i, score in enumerate(sorted_high_scores):
            high_score_text = f"{i + 1}. {score}"
            high_score_surface = self.score_font.render(high_score_text, True, (255, 0, 0))
            high_score_rect = high_score_surface.get_rect(midtop=(high_score_rect.centerx, high_score_y))
            pygame.draw.rect(self.screen, (255, 255, 255), high_score_rect, border_radius=5)
            self.screen.blit(high_score_surface, high_score_rect)
            high_score_y += 30

        restart_surface = self.score_font.render("Press 'R' to Restart or 'Q' to Quit.", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, high_score_rect.bottom + 30))
        pygame.draw.rect(self.screen, (255, 0, 0), restart_rect, border_radius=10)
        self.screen.blit(restart_surface, restart_rect)

        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.restart_game()
                        waiting_for_input = False
                    elif event.key == K_q:
                        pygame.quit()
                        return

    def restart_game(self):
        """Restart the game after fail"""
        self.snake = Snake()
        self.food = Food()
        self.spawn_food()
        self.game_start_time = 0
        self.last_eaten_time = self.game_start_time
        self.score = 0
        self.game_over = False
        self.current_track_index = 0
        pygame.mixer.music.load(self.tracks[self.current_track_index])
        pygame.mixer.music.play(-1)
        self.obstacles = []
        self.run()

    def show_settings_screen(self):
        """Settings screen"""
        running = True
        btn_scores = Button(self.screen, (0, 0, 128), 250, 225, 200, 50, 'Scores', (255, 255, 255))
        btn_quit = Button(self.screen, (128, 128, 0), 250, 375, 200, 50, 'Quit', (255, 255, 255))
        lbl_title = Label(self.screen, 'Snake Game', 100, 50, 500, 50, (255, 255, 255))

        bg_instructions = "Press '1' for BG 1, '2' for BG 2, '3' for BG 3"
        bg_instructions1 = "Press '0' to go back to default background"
        instructions_label = Label(self.screen, bg_instructions, 30, 100, 700, 50, (255, 255, 255))
        instructions_label1 = Label(self.screen, bg_instructions1, 30, 150, 700, 50, (255, 255, 255))

        high_scores_display = []

        while running:
            self.screen.fill((175, 215, 70) if self.use_default_background else (0, 0, 0))
            if not self.use_default_background:
                self.screen.blit(self.bg_image, (0, 0))
            lbl_title.draw()
            btn_scores.draw()
            btn_quit.draw()
            instructions_label.draw()
            instructions_label1.draw()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        self.use_default_background = True
                    elif event.key == K_1:
                        self.change_background(0)
                        self.use_default_background = False
                    elif event.key == K_2:
                        self.change_background(1)
                        self.use_default_background = False
                    elif event.key == K_3:
                        self.change_background(2)
                        self.use_default_background = False
                elif btn_scores.is_clicked(event):
                    high_scores_display = self.high_scores
                elif btn_quit.is_clicked(event):
                    running = False

            if high_scores_display:
                y_offset = 450
                for score in high_scores_display:
                    score_label = Label(self.screen, str(score), 250, y_offset, 200, 50, (255, 255, 255))
                    score_label.draw()
                    y_offset += 30

            pygame.display.flip()
            self.clock.tick(60)
