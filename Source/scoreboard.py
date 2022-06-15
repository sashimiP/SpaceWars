import pygame.font
from pygame.sprite import Group
import json

from ship import Ship


class Scoreboard:
    """A class to represent the HUD."""

    def __init__(self, s_w_game):
        """Initialize score keeping attributes."""
        self.s_w_game = s_w_game
        self.screen = s_w_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = s_w_game.settings
        self.stats = s_w_game.stats

        # Prepare the initial score image, level(wave), lives(ships) and high score.
        self.prep_score()
        self.prep_level()
        self.prep_lives()
        self.prep_high_score()
        self.prep_bugs_left()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        self.score_image = self.settings.hud_font.render(f"Score: {score_str}", True, self.settings.text_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 20

    def display_hud(self):
        """Draw the score, level and lives to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.lives.draw(self.screen)
        self.screen.blit(self.bugs_left_image, self.bugs_left_rect)

    def update_score(self, number):
        """
        Add a point when an enemy gets hit.
        Points vary from enemy type to enemy type;
        Calls save_score method;
        Calls check_high_score method.
         """
        self.stats.score += number
        self.save_score(self.stats.score)
        self.check_high_score(self.stats.score, self.high_score)
        self.prep_score()
        self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.settings.hud_font.render(f"Level: {level_str}", True, self.settings.text_color)

        # Position the level mid-top of screen.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.midtop = self.screen_rect.midtop
        self.level_rect.x -= 25

    def prep_lives(self):
        """Turn number of ships(lives) left into a rendered image."""
        self.lives = Group()
        for lives_number in range(self.stats.ship_lives_left):
            live = Ship(self.s_w_game)
            live.image = pygame.image.load('images/player_lives.png')
            live.rect = live.image.get_rect()
            live.rect.x = 10 + lives_number * live.rect.width
            live.rect.bottom = self.score_rect.bottom + 50
            self.lives.add(live)
            
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        try:
            with open(self.settings.high_score_filename, 'r') as f:
                self.high_score = json.load(f)
        except FileNotFoundError:
            self.high_score = 0
        high_score_str = str(self.high_score)
        self.high_score_image = self.settings.hud_font.render(
            f"High score: {high_score_str}", True, self.settings.text_color)

        # Position the high score in the top right corner of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 50
        self.high_score_rect.top = 20

    def save_score(self, last_score):
        """Saves the current score to a json file"""
        with open(self.settings.last_score_filename, 'w') as f:
            json.dump(last_score, f)
            
    def check_high_score(self, last_score, high_score):
        """
        If the current score is higher than the high_score,
        current score becomes the high score.
        """
        if last_score > high_score:
            high_score = last_score
        with open(self.settings.high_score_filename, 'w') as f:
            json.dump(high_score, f)

    def prep_bugs_left(self):
        """How enemies are left before the boss spawns."""
        bugs_left_str = str(self.stats.bugs_left)
        self.bugs_left_image = self.settings.hud_font.render(f"Bugs Left: {bugs_left_str}",
                                                             True, self.settings.text_color)
        self.bugs_left_rect = self.bugs_left_image.get_rect()
        self.bugs_left_rect.bottomleft = self.screen_rect.bottomleft
        self.bugs_left_rect.x += 20
        self.bugs_left_rect.y -= 20

    def update_bugs_left(self):
        """Update the number of enemies that the player has to kill to spawn the boss."""
        self.prep_bugs_left()
        if self.stats.bugs_left > 0:
            self.stats.bugs_left -= 1

