import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, s_w_game, position):
        """Creates a bullet object at the ship's current position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.settings = s_w_game.settings
        self.sprites_shot = [pygame.image.load('images/Shot1/shot1_1.png'),
                             pygame.image.load('images/Shot1/shot1_2.png'),
                             pygame.image.load('images/Shot1/shot1_3.png'),
                             pygame.image.load('images/Shot1/shot1_4.png')]

        self.shot_index = 0
        self.shot_image = self.sprites_shot[int(self.shot_index)]
        self.rect = self.shot_image.get_rect()
        self.rect.midright = position
        
        self.shot_x = float(self.rect.x)

    def update(self):
        """Move the bullets right toward end of screen."""
        self.shot_x += self.settings.bullet_speed

        self.rect.x = self.shot_x
        self.shot_index += 0.1
        if self.shot_index >= len(self.sprites_shot):
            self.shot_index -= 0.1
    
        self.shot_image = self.sprites_shot[int(self.shot_index)]

    def draw_bullet(self):
        """Draw the bullets to the screen."""
        self.screen.blit(self.shot_image, self.rect)
