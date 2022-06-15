
import sys
import pygame
import random
from random import randint
from time import sleep
import json

from settings import Settings
from ship import Ship
from bullet import Bullet
from bullet_exp import BulletExplosion
from enemy import Enemy
from boss import Boss
from enemy_projectile import EnemyProjectile
from asteroid import Asteroid
from game_stats import GameStats
from scoreboard import Scoreboard
from menu import Menu
from power_ups import PowerUps


class SpaceWars:
    """Overall game engine class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # Sound Effects
        # Background music
        pygame.mixer.music.load(self.settings.bg_music)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1, 34.0)

        pygame.display.set_caption("Space Wars")

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.bullets_1 = pygame.sprite.Group()
        self.bullets_exp = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group()

        self.the_boss = pygame.sprite.Group()
        self.boss_projectiles_top = pygame.sprite.Group()
        self.boss_projectiles_mid = pygame.sprite.Group()
        self.boss_projectiles_bot = pygame.sprite.Group()

        self.enemy_exp = pygame.sprite.Group()

        self.asteroids = pygame.sprite.Group()

        self.power_ups = pygame.sprite.Group()

        # HUD
        self.scoreboard = Scoreboard(self)

        self.menu = Menu(self)

        self.clock = pygame.time.Clock()

    def run_game(self):
        """Start the main game loop."""
        while True:
            self._check_event()
            if (self.stats.game_active and not self.stats.game_pause) \
                    or (self.stats.has_died) and (not self.stats.you_won):
                self._update_bullets()
                self._update_projectile_explosion(self.bullets_exp)
                self.ship.update()
                self._update_enemy()
                self._update_power_ups()
                if self.stats.spawn_boss:
                    self._update_boss()
                    self._update_boss_projectiles()
                self._update_projectile_explosion(self.enemy_exp)
                self._update_asteroid()
            self._update_screen()

    def _check_event(self):
        """Respond to key presses and more events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click = True
                self._main_menu(mouse_pos, click)
                if self.stats.game_pause:
                    self._pause_menu(mouse_pos, click)
                if self.stats.has_died:
                    self._died_menu(mouse_pos, click)
                if self.stats.you_won:
                    self._you_won_menu(mouse_pos, click)
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                click = False
                self._main_menu(mouse_pos, click)
                if self.stats.game_pause:
                    self._pause_menu(mouse_pos, click)
                if self.stats.you_won:
                    self._you_won_menu(mouse_pos, click)
                if self.stats.has_died:
                    self._died_menu(mouse_pos, click)

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen."""
        self.screen.blit(self.settings.bg_image, self.settings.bg_rect)

        if self.stats.game_active:
            if not self.stats.has_died:
                self._scroll_background()
                self.ship.draw_player()
            if not self.stats.you_won:
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                for enemy in self.enemies.sprites():
                    enemy.draw_enemy()
                self._draw_enemy_projectiles(self.boss_projectiles_top)
                self._draw_enemy_projectiles(self.boss_projectiles_mid)
                self._draw_enemy_projectiles(self.boss_projectiles_bot)
                for asteroid in self.asteroids.sprites():
                    asteroid.draw_asteroid()
                for power_up in self.power_ups.sprites():
                    power_up.draw_power_ups()
                for bullet_exp in self.bullets_exp.sprites():
                    bullet_exp.draw_explosion()
            for projectile_exp in self.enemy_exp.sprites():
                projectile_exp.draw_explosion()
            for boss in self.the_boss.sprites():
                boss.draw_boss()
            # Draw the hud
            self.scoreboard.display_hud()
            if self.stats.game_pause:
                self.menu.draw_pause_menu()
            if self.stats.has_died:
                self.menu.draw_died_menu()
            if self.stats.you_won:
                self.menu.draw_you_won_menu()
        else:
            self.menu.draw_main_menu()
        pygame.display.flip()
        self.clock.tick(self.settings.FPS)

    def _scroll_background(self):
        """Move the background toward the right side of the screen."""
        self.settings.bg_rect_x -= self.settings.screen_scroll_speed
        self.settings.bg_rect.x = self.settings.bg_rect_x

    def _check_keydown_events(self, event):
        """Responds to key presses."""
        if event.key == pygame.K_ESCAPE and not self.stats.game_pause \
                and not self.stats.has_died and self.stats.game_active \
                and not self.stats.you_won:
            self.stats.game_pause = True
            pygame.mouse.set_visible(True)
            self.settings.screen_scroll_speed = 0
        elif event.key == pygame.K_ESCAPE and self.stats.game_pause \
                and not self.stats.has_died and self.stats.game_active \
                and not self.stats.you_won:
            self.stats.game_pause = False
            pygame.mouse.set_visible(False)
            self.settings.screen_scroll_speed = 0.5
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            self.settings.screen_scroll_speed = 2
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
            self.settings.screen_scroll_speed *= (-1)
        elif event.key == pygame.K_SPACE:
            if len(self.bullets) < self.settings.bullets_allowed:
                self.settings.blaster_sound.play(loops=0)
            self._fire_bullets()

    def _check_keyup_events(self, event):
        """Responds to releasing of key."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
            self.settings.screen_scroll_speed = 0.5
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            self.settings.screen_scroll_speed = 0.5

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()
        self._sprite_leave_screen_right(self.bullets, self.screen.get_rect().right)

        self._check_bullet_alien_collisions()
        self._check_bullet_asteroid_collisions()
        self._check_bullet_boss_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Check for any bullets that have hit aliens.
          If so, get rid of the bullets and the alien.
        """
        for bullet in self.bullets.copy():
            for enemy in self.enemies.copy():
                if bullet.rect.colliderect(enemy):
                    self.settings.enemy_hit_sound.play(loops=0)
                    self.scoreboard.update_score(1)
                    self._spawn_explosion(self.bullets_exp, self.settings.bullet_frames,
                                          bullet.rect.x, bullet.rect.y, 0.5)
                    self._spawn_explosion(self.enemy_exp, self.settings.enemy_death, enemy.rect.x, enemy.rect.y, 0.5)
                    self.scoreboard.update_bugs_left()

        pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)

    def _create_enemy(self):
        """Create the enemies"""
        enemy = Enemy(self, 'images/alien_1.png', 200, self.settings.enemy_speed)
        if self.settings.enemies_allowed > len(self.enemies) and not self.stats.spawn_boss:
            enemy_type = randint(0, self.settings.enemies_allowed)
            enemy_position_y = randint(enemy.rect.height, self.settings.screen_height - enemy.rect.height * 2)
            speed = random.uniform(3.0, self.settings.enemy_speed)
            new_enemy = Enemy(self, self.settings.enemy_types[enemy_type], speed, enemy_position_y)
            self.enemies.add(new_enemy)

    def _update_enemy(self):
        """Update the position of the enemies"""
        self._create_enemy()
        self.enemies.update()
        self._sprite_leave_screen_left(self.enemies, -30)
        if self.stats.bugs_left == 20:
            self.stats.spawn_upgrade_weapon = True
        if self.stats.bugs_left <= 0:
            self.stats.spawn_boss = True

    # Change in the future!!!!
    def _ship_edge_hit(self, sprite_group, sprite):
        """
        Respond to the ship being hit by an object
         or edge being hit by an enemy.
         """
        sprite_group.remove(sprite)
        if isinstance(sprite, Enemy) and not self.stats.has_died:
            self.settings.enemy_hit_sound.play(loops=0)
            self._spawn_explosion(self.enemy_exp, self.settings.enemy_death, sprite.rect.x, sprite.rect.y, 0.5)
        if isinstance(sprite, Asteroid):
            self.settings.ship_asteroid_hit.play()
            self._spawn_explosion(self.enemy_exp, self.settings.asteroid_exp_frames,
                                  sprite.rect.x, sprite.rect.y - 25, 0.6)
        if isinstance(sprite, PowerUps):
            self.settings.upgrade_weapon_sound.play(loops=0)
            self.stats.upgrade_weapon = True
            self.settings.bullets_allowed = 10

        # if the object is not a power-up, decrement ships_left
        if not self.stats.you_won and not isinstance(sprite, PowerUps):
            if self.stats.ship_lives_left > 0:
                self.stats.ship_lives_left -= 1
                self.scoreboard.prep_lives()

            else:
                self.ship.x = - 1000
                self.settings.player_died_sound.play(loops=0)
                self.stats.has_died = True
                pygame.mouse.set_visible(True)

            if not self.stats.has_died:
                # Lag when hit.
                sleep(0.10)

    def _create_asteroid(self):
        """Create the asteroids."""
        asteroid = Asteroid(self, 200, self.settings.asteroid_speed)
        if self.settings.asteroids_allowed > len(self.asteroids):
            asteroid_position_y = self.ship.rect.y
            asteroid_speed = random.uniform(5.0, self.settings.asteroid_speed)
            new_asteroid = Asteroid(self, asteroid_position_y, asteroid_speed)
            random_asteroid_pos_y = randint(
                asteroid.rect.height, self.settings.screen_height - asteroid.rect.height * 2)
            random_asteroid_speed = random.uniform(3.0, 5.0)
            random_asteroid = Asteroid(self, random_asteroid_pos_y, random_asteroid_speed)
            self.asteroids.add(new_asteroid)
            self.asteroids.add(random_asteroid)

    def _update_asteroid(self):
        """Update the position of the asteroids."""
        self._create_asteroid()
        self.asteroids.update()

        self._sprite_leave_screen_left(self.asteroids, -1000)

    def _check_bullet_asteroid_collisions(self):
        """
        Check for any bullets that have hit asteroids.
          If so, get rid of the bullets.
        """
        for bullet in self.bullets.copy():
            for asteroid in self.asteroids.copy():
                if bullet.rect.colliderect(asteroid):
                    self.settings.blaster_proj_hit_sound.play(loops=0)
                    self._spawn_explosion(self.bullets_exp,
                                          self.settings.bullet_frames, bullet.rect.x, bullet.rect.y, 0.5)
        pygame.sprite.groupcollide(self.bullets, self.asteroids, True, False)
        self._check_boss_proj_object_collisions(self.boss_projectiles_top, self.asteroids, True)
        self._check_boss_proj_object_collisions(self.boss_projectiles_mid, self.asteroids, True)
        self._check_boss_proj_object_collisions(self.boss_projectiles_bot, self.asteroids, True)

    def _update_projectile_explosion(self, projectile_exp_group):
        """Update the bullet explosion frames"""
        for projectile_exp in projectile_exp_group.copy():
            projectile_exp.update_explosion()
            if projectile_exp.animation_end:
                projectile_exp_group.remove(projectile_exp)

    def _spawn_explosion(self, sprite_group, animation_frames, sprite_x, sprite_y, frame_rate):
        """Animate explosion frames."""
        explosion = BulletExplosion(self, animation_frames, sprite_x, sprite_y, frame_rate)
        sprite_group.add(explosion)

    def _create_boss(self):
        """Create the boss enemy."""
        if len(self.the_boss) < 1 and self.stats.spawn_boss and not self.stats.you_won:
            self.settings.spawn_boss_sound.play(loops=0)
            boss = Boss(self)
            self.the_boss.add(boss)

    def _update_boss(self):
        """Update the position of the boss."""
        self._create_boss()
        self.the_boss.update()
        if not self.stats.has_died:
            for boss in self.the_boss.copy():
                self._fire_boss_projectiles(boss.rect.topleft,
                                            boss.rect.midleft,
                                            boss.rect.bottomleft)
                if boss.h_p <= 0:
                    self._boss_death(self.enemy_exp, self.settings.boss_death_frames,
                                     boss.rect.x, boss.rect.y)

    def _check_bullet_boss_collisions(self):
        """
        Check if any bullets hit the boss enemy.
        If collision takes place, take a hp point away from boss,
        remove bullet sprite,
        and call bullet explosion method.
        """
        for bullet in self.bullets.copy():
            for boss in self.the_boss.copy():
                if bullet.rect.colliderect(boss):
                    self.settings.hit_boss.play(loops=0)
                    self._spawn_explosion(self.bullets_exp,
                                          self.settings.bullet_frames, bullet.rect.x, bullet.rect.y, 0.5)
                    boss.h_p -= 1
                    self.scoreboard.update_score(2)
        pygame.sprite.groupcollide(self.bullets, self.the_boss, True, False)

    def _fire_bullets(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed and not self.stats.upgrade_weapon:
            new_bullet = Bullet(self, self.ship.rect.midright)
            self.bullets.add(new_bullet)
        elif len(self.bullets) < self.settings.bullets_allowed and self.stats.upgrade_weapon:
            new_bullet_1 = Bullet(self, self.ship.rect.midright)
            new_bullet_2 = Bullet(self, self.ship.rect.bottomright)
            self.bullets.add(new_bullet_1)
            self.bullets.add(new_bullet_2)

    def _fire_boss_projectiles(self, topleft, midleft, bottomleft):
        """Create a new boss projectile and add it to the boss projectile group."""
        for boss in self.the_boss.copy():
            if boss.h_p > 60:
                if boss.go_down and not boss.go_up:
                    projectile_speed = self.settings.boss_projectile_speed / 2
                    self._fire_projectiles(self.boss_projectiles_top, topleft,
                                           projectile_speed, self.settings.boss_fire_weapon_sound)
                    self._fire_projectiles(self.boss_projectiles_mid, midleft,
                                           projectile_speed, self.settings.boss_fire_weapon_sound)
                    self._fire_projectiles(self.boss_projectiles_bot, bottomleft,
                                           projectile_speed, self.settings.boss_fire_weapon_sound)
            else:
                if boss.h_p > 30:
                    projectile_speed = self.settings.boss_projectile_speed / 2
                else:
                    projectile_speed = self.settings.boss_projectile_speed / 2
                self._fire_projectiles(self.boss_projectiles_top, topleft,
                                       projectile_speed, self.settings.boss_fire_weapon_sound)
                self._fire_projectiles(self.boss_projectiles_mid, midleft,
                                       projectile_speed, self.settings.boss_fire_weapon_sound)
                self._fire_projectiles(self.boss_projectiles_bot, bottomleft,
                                       projectile_speed, self.settings.boss_fire_weapon_sound)

    def _fire_projectiles(self, projectile_group, projectile_starting_position,
                          projectile_speed, fire_sound):
        """Create a new projectile and add it to the projectile group."""
        if len(projectile_group) < self.settings.boss_projectiles:
            fire_sound.play()
            new_projectile = EnemyProjectile(self, self.settings.boss_projectile_frames,
                                             projectile_speed,
                                             projectile_starting_position)
            projectile_group.add(new_projectile)

    def _update_boss_projectiles(self):
        """Update the boss projectile's position and get rid of projectiles that leave screen."""
        self._check_boss_proj_object_collisions(self.boss_projectiles_top, self.ship, False)
        self._check_boss_proj_object_collisions(self.boss_projectiles_mid, self.ship, False)
        self._check_boss_proj_object_collisions(self.boss_projectiles_bot, self.ship, False)

        self.boss_projectiles_top.update()
        self.boss_projectiles_mid.update()
        self.boss_projectiles_bot.update()

    def _check_boss_proj_object_collisions(self, projectile_group, sprite_group, group=False):
        """If boss projectiles hit player spawn explosion and take hp point."""
        for projectile in projectile_group.copy():
            if group:
                for sprite in sprite_group.copy():
                    if projectile.rect.colliderect(sprite):
                        self.settings.boss_proj_hit_sound.play(loops=0)
                        self._spawn_explosion(self.enemy_exp,
                                              self.settings.boss_exp_frames,
                                              projectile.rect.x - 150,
                                              projectile.rect.y - 150, 0.6)
                pygame.sprite.groupcollide(projectile_group, sprite_group, True, True)
            else:
                if projectile.rect.colliderect(sprite_group):
                    self.settings.boss_proj_hit_sound.play(loops=0)
                    self._spawn_explosion(self.enemy_exp, self.settings.boss_exp_frames,
                                          projectile.rect.x - 150, projectile.rect.y - 150, 0.6)
                self._sprite_leave_screen_left(projectile_group, 0)

    def _remove_boss_projectiles(self):
        """Removes all boss_projectiles from the screen."""
        self.boss_projectiles_top.empty()
        self.boss_projectiles_mid.empty()
        self.boss_projectiles_bot.empty()

    def _draw_enemy_projectiles(self, sprite_group):
        """Draw the enemy projectile to the screen."""
        for sprite in sprite_group.sprites():
            sprite.draw_enemy_projectile()

    def _sprite_leave_screen_left(self, sprite_group, border):
        """
        Remove sprites from groups that have left the screen from the left side,
        or have collided with the ship.
        """
        for sprite in sprite_group.copy():
            if sprite.rect.right < border:
                sprite_group.remove(sprite)
                if isinstance(sprite, Enemy):
                    self._ship_edge_hit(sprite_group, sprite)
                    self.scoreboard.update_bugs_left()
                if isinstance(sprite, PowerUps):
                    self.stats.upgrade_weapon_left_screen = True
            # Look for ship-object collisions.
            if pygame.sprite.spritecollideany(self.ship, sprite_group):
                self._ship_edge_hit(sprite_group, sprite)

    def _sprite_leave_screen_right(self, sprite_group, border):
        """
        Remove sprites from groups that have left the screen from the right side,
        or have collided with the ship.
        """
        for sprite in sprite_group.copy():
            if sprite.rect.left >= border:
                sprite_group.remove(sprite)

    def _boss_death(self, sprite_group, animation_frames, sprite_x, sprite_y):
        """Spawns explosions at the boss's position."""
        self.settings.boss_death_sound.play(loops=0)

        self.scoreboard.update_score(40)

        self._remove_boss_projectiles()

        self.the_boss.empty()

        self._spawn_explosion(sprite_group, animation_frames,
                              sprite_x - 250, sprite_y - 150, 0.3)

        self.stats.spawn_boss = False

        self.stats.you_won = True

    def _create_power_up(self):
        """Create the power-ups."""
        power_up = PowerUps(self, self.settings.power_ups_lst[0],
                            self.settings.power_ups_speed, 200)
        if self.stats.spawn_upgrade_weapon and len(self.power_ups) < 1 \
                and not self.stats.upgrade_weapon and not self.stats.upgrade_weapon_left_screen:
            power_up_type = self.settings.power_ups_lst[self.settings.UPGRADE_WEAPON]
            power_up_position_y = randint(power_up.rect.height, self.settings.screen_height - power_up.rect.height * 2)
            speed = self.settings.power_ups_speed
            new_power_up = PowerUps(self, power_up_type, speed, power_up_position_y)
            self.power_ups.add(new_power_up)

    def _update_power_ups(self):
        """Update the position of the power-ups."""
        self._create_power_up()
        self.power_ups.update()
        self._sprite_leave_screen_left(self.power_ups, -30)

    def _main_menu(self, mouse_pos, click):
        """
        Initializes the main menu methods.
        """
        self._check_play_button(mouse_pos, click)
        self._check_exit_button(mouse_pos, click)

    def _check_play_button(self, mouse_pos, click):
        """Start game when the plater clicks "Play"."""
        play_button_clicked = self.menu.play_rect.collidepoint(mouse_pos)
        if play_button_clicked and click and not self.stats.game_active:
            self._restart_game(False, True, False)
        elif self.menu.play_rect.collidepoint(mouse_pos) and not click:
            self.menu.play_button_color = self.settings.hoover_color
        else:
            self.menu.play_button_color = self.settings.text_color

    def _check_exit_button(self, mouse_pos, click):
        """Exit when the player clicks "Exit"."""
        exit_button_clicked = self.menu.exit_rect.collidepoint(mouse_pos)
        if exit_button_clicked and click and not self.stats.game_active:
            self.stats.game_active = False
            sys.exit()
        elif self.menu.exit_rect.collidepoint(mouse_pos) and not click:
            self.menu.exit_button_color = self.settings.hoover_color
        else:
            self.menu.exit_button_color = self.settings.text_color

    def _pause_menu(self, mouse_pos, click):
        """Initializes the pause menu methods."""
        self._check_continue_button(mouse_pos, click)
        self._check_restart_button(mouse_pos, click)
        self._check_quit_button(mouse_pos, click)

    def _check_continue_button(self, mouse_pos, click):
        """Continue the game when player clicks "Continue"."""
        continue_button_clicked = self.menu.continue_rect.collidepoint(mouse_pos)
        if continue_button_clicked and click and self.stats.game_active:
            self.stats.game_pause = False
            self.settings.screen_scroll_speed = 0.5
            pygame.mouse.set_visible(False)
        elif self.menu.exit_rect.collidepoint(mouse_pos) and not click:
            self.menu.continue_button_color = self.settings.hoover_color
        else:
            self.menu.continue_button_color = self.settings.text_color

    def _check_restart_button(self, mouse_pos, click):
        """Restarts the level when the player clicks on "Restart Level"."""
        restart_button_clicked = self.menu.restart_rect.collidepoint(mouse_pos)
        if restart_button_clicked and click and self.stats.game_active:
            self._restart_game(False, True)
        elif self.menu.restart_rect.collidepoint(mouse_pos) and not click:
            self.menu.restart_button_color = self.settings.hoover_color
        else:
            self.menu.restart_button_color = self.settings.text_color

    def _check_quit_button(self, mouse_pos, click):
        """
        Returns to main menu when the player clicks on "Quit",
        and resets the game.
        """
        quit_button_clicked = self.menu.quit_rect.collidepoint(mouse_pos)
        if quit_button_clicked and click and self.stats.game_active:
            self._restart_game(True)
        elif self.menu.quit_rect.collidepoint(mouse_pos) and not click:
            self.menu.quit_button_color = self.settings.hoover_color
        else:
            self.menu.quit_button_color = self.settings.text_color

    def _died_menu(self, mouse_pos, click):
        """Initializes menu for when player runs out of lives."""
        self._check_restart_button(mouse_pos, click)
        self._check_quit_button(mouse_pos, click)

    def _you_won_menu(self, mouse_pos, click):
        """Initializes the pause menu methods."""
        pygame.mouse.set_visible(True)
        self._check_restart_button(mouse_pos, click)
        self._check_quit_button(mouse_pos, click)

    def _restart_game(self, mouse_visible=False, game_active=False, game_pause=False):
        """
        Resets the game stats.
        Removes all sprites from screen.
        Player returned to starting position.
        """
        pygame.mouse.set_visible(mouse_visible)
        self.stats.game_active = game_active
        self.stats.game_pause = game_pause
        self.stats.reset_stats()
        self.ship.center_player()
        self.enemies.empty()
        self.asteroids.empty()
        self.bullets.empty()
        self.the_boss.empty()
        self.enemy_exp.empty()
        self._remove_boss_projectiles()
        self.scoreboard.update_score(0)
        self.scoreboard.prep_lives()
        self.scoreboard.update_bugs_left()


s_w = SpaceWars()
s_w.run_game()
