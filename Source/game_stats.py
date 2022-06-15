import json


class GameStats:
    """Track statistics for Space Wars."""

    def __init__(self, s_w_game):
        """Initialize statistics."""
        self.settings = s_w_game.settings
        self.reset_stats()
        # Start Space Wars in an active state.
        self.game_active = False
        self.game_pause = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_lives_left = self.settings.ship_lives_limit
        self.score = 0
        self.level = 1
        self.has_died = False
        self.spawn_boss = False
        self.bugs_left = self.settings.bugs_left_lv_one
        self.you_won = False
        self.upgrade_weapon = False
        self.spawn_upgrade_weapon = False
        self.upgrade_weapon_left_screen = False
        self.settings.bullets_allowed = 4
        self.settings.screen_scroll_speed = 0.5
        
        