import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):
    """A class to represent a single enemy."""

    def __init__(self, s_w_game, image, speed, y_position):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings
        self.speed = speed

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect().inflate(-30, -45)
        # self.rect_color = (255, 0, 0)
        
        self.frames = self.settings.enemy_frames[:]
        self.frame_index = 0
        # Start each new enemy at the right side of the screen.
        self.rect.x = self.screen.get_rect().width - self.rect.width
        self.rect.y = float(y_position)

        # Store the enemy's exact vertical position
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien left toward end of screen."""
        # Update the decimal position of the enemy.
        self.x -= self.speed
        # Update the rect position.
        self.rect.x = self.x

        self.animate_movement()
        
    def animate_movement(self):
        """Animate the movement of the enemies."""
        self.frame_index += 0.04 * self.speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def draw_enemy(self):
        """Draw the enemy at its current location."""
        # pygame.draw.rect(self.screen, self.rect_color, self.rect)
        self.screen.blit(self.image, self.rect)

