import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    """A class to represent a single asteroid."""

    def __init__(self, s_w_game, y_position, speed):
        """Initialize the asteroid and set its starting position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings
        self.speed = speed

        # Load the asteroid frames and set its rect attributes.
        self.frames = self.settings.asteroid_frames[:]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect().inflate(-20, -25)
        # self.rect_color = (255, 0, 0)

        # Start each new asteroid on the right side of the screen.
        self.rect.x = self.screen.get_rect().width
        self.rect.y = float(y_position)

        # Store the asteroids exact vertical position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the asteroid left toward end of screen."""

        # Update the decimal position of the asteroid.
        self.x -= self.speed

        # Update the rect position.
        self.rect.x = self.x

        self.frame_index += 0.15
        if self.frame_index >= (len(self.frames)):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def draw_asteroid(self):
        """Draws the asteroid to the screen."""
        # pygame.draw.rect(self.screen, self.rect_color, self.rect)
        self.screen.blit(self.image, self.rect)

