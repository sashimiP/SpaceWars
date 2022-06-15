import pygame
from pygame.sprite import Sprite

class EnemyProjectile(Sprite):
    """A class to manage the enemy's projectiles."""
    def __init__(self, s_w_game, projectile_frames, projectile_speed, rect_midleft):
        super().__init__()
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.speed = projectile_speed

        self.frames = projectile_frames[:]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = pygame.Rect(self.image.get_rect().x, self.image.get_rect().y, 70, 20)

        self.rect.midleft = rect_midleft
        self.x = float(self.rect.x)

        # self.rect_color = (255, 0, 0)

    def update(self):
        """Move the enemy projectile left toward end of screen."""
        self.x -= self.speed
        self.rect.x = self.x

        self.frame_index += 0.4
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1

        self.image = self.frames[int(self.frame_index)]

    def draw_enemy_projectile(self):
        """Draw the enemy's projectile ot the screen."""
        # pygame.draw.rect(self.screen, self.rect_color, self.rect)
        self.screen.blit(self.image, self.rect)
