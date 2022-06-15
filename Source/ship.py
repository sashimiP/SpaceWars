import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the player."""

    def __init__(self, s_w_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings
        
        self.mov_frames = [pygame.image.load('images/player_movement/player1.png'),
                           pygame.image.load('images/player_movement/player2.png'),
                           pygame.image.load('images/player_movement/player3.png'),
                           pygame.image.load('images/player_movement/player4.png')]

        self.turbo_frames = [pygame.image.load('images/player_turbo/player1.png'),
                             pygame.image.load('images/player_turbo/player2.png'),
                             pygame.image.load('images/player_turbo/player3.png'),
                             pygame.image.load('images/player_turbo/player4.png')]

        self.mov_index = 0
        self.turbo_index = 0
        
        self.image = pygame.image.load('images/player.png')
        self.rect = self.image.get_rect().inflate(-10, -40)
        # self.rect_color = (255, 0, 0)

        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flags."""
        self.animate_movement()

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self.turbo_movement()
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.y = self.y
        self.rect.x = self.x

    def draw_player(self):
        """Draw the ship at its current position."""
        # pygame.draw.rect(self.screen, self.rect_color, self.rect)
        self.screen.blit(self.image, self.rect)

    def animate_movement(self):
        """Animate basic ship exhaust animation."""
        self.mov_index += 0.1
        if self.mov_index >= len(self.mov_frames):
            self.mov_index = 0

        self.image = self.mov_frames[int(self.mov_index)]

    def turbo_movement(self):
        """Animate forward ship exhaust animation."""
        self.turbo_index += 0.1
        if self.turbo_index >= len(self.turbo_frames):
            self.turbo_index = 0

        self.image = self.turbo_frames[int(self.turbo_index)]

    def center_player(self):
        """Center the ship on the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


