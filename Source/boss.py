import pygame
from pygame.sprite import Sprite


class Boss(Sprite):
    """A class to manage the boss enemy."""

    def __init__(self, s_w_game):
        """Initialize the boss and set his starting position."""
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings
        self.speed = self.settings.boss_speed
        self.h_p = self.settings.boss_health

        self.frames = self.settings.boss_frames[:]

        self.mov_index = 0

        self.image = self.frames[self.mov_index]
        self.rect = self.image.get_rect()

        self.rect.midright = self.screen_rect.midright
        self.rect.x += 1050

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.go_down = False
        self.go_up = False

    def update(self):
        """Update the boss's movement."""
        self.animate_movement()

        if self.rect.x >= 1000:
            self.x -= self.speed / 2
        else:
            self.go_down = True
        if self.go_down:
            self.y += self.speed
            if self.rect.y >= self.screen_rect.bottom - 300:
                self.go_down = False
                self.go_up = True
        if self.go_up:
            self.y -= self.speed * 2
            if self.rect.top <= self.screen_rect.top:
                self.go_down = True
                self.go_up = False

        self.rect.x = self.x
        self.rect.y = self.y

    def draw_boss(self):
        """Draw the boss to the screen."""
        self.screen.blit(self.image, self.rect)

    def animate_movement(self):
        """Animate the boss's movement."""
        self.mov_index += 0.1
        if self.mov_index >= len(self.frames):
            self.mov_index = 0

        self.image = self.frames[int(self.mov_index)]