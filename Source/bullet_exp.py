import pygame
from pygame.sprite import Sprite


class BulletExplosion(Sprite):
    """A class to represent bullet collision explosions."""

    def __init__(self, s_w_game, bullet_frames, x_position, y_position, frame_rate):
        """Initialize the explosions and set its starting position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings

        # Load the explosion frames and set its rect attributes.
        self.frames = bullet_frames[:]

        self.frame_index = 0
        self.frame_rate = frame_rate
        self.animation_end = False
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def update_explosion(self):
        """Animate the explosion."""
        self.frame_index += self.frame_rate
        if self.frame_index >= (len(self.frames)):
            self.animation_end = True
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def draw_explosion(self):
        """Draws the explosion to the screen."""
        self.screen.blit(self.image, self.rect)
