import pygame
from pygame.sprite import Sprite


class PowerUps(Sprite):
    """A class to manage the power ups in the game"""
    def __init__(self, s_w_game, image, speed, y_position):
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings
        self.stats = s_w_game.stats

        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.y = float(y_position)
        self.rect.x = self.screen.get_rect().width - self.rect.width
        self.x = float(self.rect.x)

    def update(self):
        """Update the power-up's movement and position."""
        self.x -= self.speed
        self.rect.x = self.x

    def draw_power_ups(self):
        """Draw the power-up ot the screen."""
        self.screen.blit(self.image, self.rect)

