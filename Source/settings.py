import pygame
import json

# REMEMBER TO CHANGE BACK bugs_left
# and
# boss_h_p


class Settings:
    """Initialize the game's settings."""

    def __init__(self):
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_image = pygame.image.load('images/Background_space.png')
        self.bg_rect = self.bg_image.get_rect()
        self.bg_rect_x = float(self.bg_rect.x)
        self.screen_scroll_speed = 0.5
        self.FPS = 60

        # Sound effects
        # Background music
        self.bg_music = 'sounds/background.mp3'
        # Player sound effects
        self.blaster_sound = pygame.mixer.Sound('sounds/player_blaster.mp3')
        self.blaster_proj_hit_sound = pygame.mixer.Sound('sounds/blaster_proj_hit.mp3')
        self.blaster_proj_hit_sound.set_volume(0.6)
        self.upgrade_weapon_sound = pygame.mixer.Sound('sounds/upgrade_weapon.mp3')
        self.player_died_sound = pygame.mixer.Sound('sounds/player_died.mp3')
        # Asteroid sound effects
        self.ship_asteroid_hit = pygame.mixer.Sound('sounds/ship_asteroid_hit.mp3')
        # Enemy sound effects
        self.enemy_proj_hit = pygame.mixer.Sound('sounds/enemy_proj_hit.mp3')
        self.enemy_hit_sound = pygame.mixer.Sound('sounds/enemy_hit.mp3')
        self.enemy_hit_sound.set_volume(0.5)
        # Boss sound effects
        self.hit_boss = pygame.mixer.Sound('sounds/blaster_proj_hit.mp3')
        self.boss_proj_hit_sound = pygame.mixer.Sound('sounds/enemy_proj_hit.mp3')
        self.spawn_boss_sound = pygame.mixer.Sound('sounds/boss_arrives.mp3')
        self.boss_fire_weapon_sound = pygame.mixer.Sound('sounds/boss_fire_sound.mp3')
        self.boss_fire_weapon_sound.set_volume(0.3)
        self.boss_death_sound = pygame.mixer.Sound('sounds/boss_death.mp3')
       
        

        # Ship settings
        self.ship_speed = 13.0
        self.ship_lives_limit = 3

        # Player Bullet settings
        self.bullet_speed = 10.0
        self.bullet_width = 15
        self.bullet_height = 6
        self.bullet_color = (254, 226, 62)
        self.bullets_allowed = 4

        self.bullet_frames = [pygame.image.load('images/Shot1/shot1_exp0.png'),
                              pygame.image.load('images/Shot1/shot1_exp1.png'),
                              pygame.image.load('images/Shot1/shot1_exp2.png'),
                              pygame.image.load('images/Shot1/shot1_exp3.png'),
                              pygame.image.load('images/Shot1/shot1_exp4.png')]

        # Enemy settings
        self.enemy_frames = [pygame.image.load('images/alien_movement/alien_1.png'),
                             pygame.image.load('images/alien_movement/alien_2.png'),
                             pygame.image.load('images/alien_movement/alien_3.png'),
                             pygame.image.load('images/alien_movement/alien_4.png'),
                             pygame.image.load('images/alien_movement/alien_5.png'),
                             pygame.image.load('images/alien_movement/alien_6.png'),
                             pygame.image.load('images/alien_movement/alien_7.png'),
                             pygame.image.load('images/alien_movement/alien_8.png')]

        self.enemy_death = [pygame.image.load('images/alien_movement/alien_death1.png'),
                            pygame.image.load('images/alien_movement/alien_death2.png'),
                            pygame.image.load('images/alien_movement/alien_death3.png'),
                            pygame.image.load('images/alien_movement/alien_death4.png'),
                            pygame.image.load('images/alien_movement/alien_death5.png'),
                            pygame.image.load('images/alien_movement/alien_death6.png')]

        self.enemy_types = ('images/alien_1.png', 'images/alien_1.png',
                            'images/alien_1.png', 'images/alien_1.png',
                            'images/alien_1.png'
                            )
        self.enemies_allowed = 4
        self.enemy_speed = 6.5
        self.bugs_left_lv_one = 50  # MUST BE 50

        # Font settings.
        self.text_color = (161, 238, 48)
        self.hoover_color = (110, 17, 81)
        self.hud_font_size = 45
        self.hud_font = pygame.font.Font('font/Grand9K Pixel.ttf', self.hud_font_size)

        self.title_font_size = 60
        self.title_font = pygame.font.Font('font/Grand9K Pixel.ttf', self.title_font_size)

        self.button_font_size = 50
        self.button_font = pygame.font.Font('font/Grand9K Pixel.ttf', self.button_font_size)

        # Asteroid settings
        self.asteroids_allowed = 1
        self.asteroid_speed = 10.0

        self.asteroid_frames = [pygame.image.load('images/asteroid/asteroid1.png'),
                                pygame.image.load('images/asteroid/asteroid2.png'),
                                pygame.image.load('images/asteroid/asteroid3.png'),
                                pygame.image.load('images/asteroid/asteroid4.png'),
                                pygame.image.load('images/asteroid/asteroid5.png'),
                                pygame.image.load('images/asteroid/asteroid6.png'),
                                pygame.image.load('images/asteroid/asteroid7.png'),
                                pygame.image.load('images/asteroid/asteroid8.png'),
                                pygame.image.load('images/asteroid/asteroid9.png')]

        self.asteroid_exp_frames = [pygame.image.load('images/asteroid/asteroid_exp1.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp2.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp3.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp4.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp5.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp6.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp7.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp8.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp9.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp10.png'),
                                    pygame.image.load('images/asteroid/asteroid_exp11.png')]

        # Power Ups Settings
        self.UPGRADE_WEAPON = 0
        self.EXTRA_LIFE = 1
        self.FIRE_WEAPON = 2
        self.lIGHTNING_WEAPON = 3
        self.VOID_WEAPON = 4

        self.power_ups_lst = [pygame.image.load('images/power_ups/up_weapon.png')]
        self.power_ups_speed = 5.0

        # High score settings
        self.last_score_filename = 'high_score/last_score.json'
        self.high_score_filename = 'high_score/high_score.json'

        # Bullet hit flag
        self.bullet_hit = False

        # Boss enemy settings
        self.boss_speed = 6.5
        self.boss_health = 100  # Must be 100
        self.boss_projectiles = 1
        self.boss_projectile_speed = 30.0

        self.boss_frames = [pygame.image.load('images/level_1_boss/boss1.png'),
                            pygame.image.load('images/level_1_boss/boss2.png'),
                            pygame.image.load('images/level_1_boss/boss3.png'),
                            pygame.image.load('images/level_1_boss/boss4.png'),
                            pygame.image.load('images/level_1_boss/boss5.png'),
                            pygame.image.load('images/level_1_boss/boss6.png'),
                            pygame.image.load('images/level_1_boss/boss7.png'),
                            pygame.image.load('images/level_1_boss/boss8.png'),
                            pygame.image.load('images/level_1_boss/boss9.png'),
                            pygame.image.load('images/level_1_boss/boss10.png'),
                            pygame.image.load('images/level_1_boss/boss11.png'),
                            pygame.image.load('images/level_1_boss/boss12.png')]

        self.boss_projectile_frames = [pygame.image.load('images/level_1_boss/shot1.png'),
                                       pygame.image.load('images/level_1_boss/shot2.png'),
                                       pygame.image.load('images/level_1_boss/shot3.png'),
                                       pygame.image.load('images/level_1_boss/shot4.png'),
                                       pygame.image.load('images/level_1_boss/shot5.png')]

        self.boss_exp_frames = [pygame.image.load('images/level_1_boss/exp1.png'),
                                pygame.image.load('images/level_1_boss/exp2.png'),
                                pygame.image.load('images/level_1_boss/exp3.png'),
                                pygame.image.load('images/level_1_boss/exp4.png'),
                                pygame.image.load('images/level_1_boss/exp5.png'),
                                pygame.image.load('images/level_1_boss/exp6.png'),
                                pygame.image.load('images/level_1_boss/exp7.png'),
                                pygame.image.load('images/level_1_boss/exp8.png'),
                                pygame.image.load('images/level_1_boss/exp9.png'),
                                pygame.image.load('images/level_1_boss/exp10.png')]

        self.boss_death_frames = [pygame.image.load('images/level_1_boss/boss_death1.png'),
                                  pygame.image.load('images/level_1_boss/boss_death2.png'),
                                  pygame.image.load('images/level_1_boss/boss_death3.png'),
                                  pygame.image.load('images/level_1_boss/boss_death4.png'),
                                  pygame.image.load('images/level_1_boss/boss_death5.png'),
                                  pygame.image.load('images/level_1_boss/boss_death6.png'),
                                  pygame.image.load('images/level_1_boss/boss_death7.png'),
                                  pygame.image.load('images/level_1_boss/boss_death8.png'),
                                  pygame.image.load('images/level_1_boss/boss_death9.png'),
                                  pygame.image.load('images/level_1_boss/boss_death10.png'),
                                  pygame.image.load('images/level_1_boss/boss_death11.png'),
                                  pygame.image.load('images/level_1_boss/boss_death12.png'),
                                  pygame.image.load('images/level_1_boss/boss_death13.png'),
                                  pygame.image.load('images/level_1_boss/boss_death14.png'),
                                  pygame.image.load('images/level_1_boss/boss_death15.png'),
                                  pygame.image.load('images/level_1_boss/boss_death16.png'),
                                  pygame.image.load('images/level_1_boss/boss_death17.png'),
                                  pygame.image.load('images/level_1_boss/boss_death18.png'),
                                  pygame.image.load('images/level_1_boss/boss_death19.png'),
                                  pygame.image.load('images/level_1_boss/boss_death20.png'),
                                  ]
