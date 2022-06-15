import pygame


class Menu:
    """A class to manage the main meny."""
    def __init__(self, s_w_game):
        self.screen = s_w_game.screen
        self.screen_rect = s_w_game.screen.get_rect()
        self.settings = s_w_game.settings

        self.play_button_color = self.settings.text_color
        self.continue_button_color = self.settings.text_color
        self.restart_button_color = self.settings.text_color
        self.quit_button_color = self.settings.text_color
        self.exit_button_color = self.settings.text_color

        self.game_title_image = self.settings.title_font.render("Space Wars", True, self.settings.text_color)
        self.died_title_image = self.settings.title_font.render("YOU ARE DEAD", True, self.settings.text_color)
        self.you_won_title_image = self.settings.title_font.render("YOU WON", True, self.settings.text_color)
        self.main_menu_image = self.settings.title_font.render("Main Menu", True, self.settings.text_color)
        self.play_button_image = self.settings.button_font.render("Play", True, self.play_button_color)
        self.continue_button_image = self.settings.button_font.render("Continue", True, self.continue_button_color)
        self.restart_button_image = self.settings.button_font.render("Restart Level", True, self.restart_button_color)
        self.quit_button_image = self.settings.button_font.render("Quit Game", True, self.quit_button_color)
        self.exit_button_image = self.settings.button_font.render("Exit", True, self.exit_button_color)
        self.game_pause_image = self.settings.title_font.render("Game Paused", True, self.settings.text_color)

        self.game_title_rect = self.game_title_image.get_rect()
        self.game_title_rect.midtop = self.screen_rect.midtop

        self.died_title_rect = self.died_title_image.get_rect()
        self.you_won_rect = self.you_won_title_image.get_rect()
        self.main_menu_rect = self.main_menu_image.get_rect()
        self.play_rect = self.play_button_image.get_rect()
        self.continue_rect = self.continue_button_image.get_rect()
        self.restart_rect = self.restart_button_image.get_rect()
        self.quit_rect = self.quit_button_image.get_rect()
        self.exit_rect = self.exit_button_image.get_rect()
        self.game_pause_rect = self.game_pause_image.get_rect()
        
    def prep_main_menu(self):
        """Format the main menu."""
        self.play_button_image = self.settings.button_font.render("Play", True, self.play_button_color)
        self.exit_button_image = self.settings.button_font.render("Exit", True, self.exit_button_color)

        self.main_menu_rect.center = self.screen_rect.center
        self.main_menu_rect.y -= 150

        self.play_rect.center = self.screen_rect.center
        self.play_rect.y -= 50
        
        self.exit_rect.center = self.screen_rect.center
        self.exit_rect.y += self.play_rect.height - 50
        
    def prep_pause_menu(self):
        """Format the pause menu."""
        self.continue_button_image = self.settings.button_font.render("Continue", True, self.continue_button_color)
        self.restart_button_image = self.settings.button_font.render("Restart Level", True, self.restart_button_color)
        self.quit_button_image = self.settings.button_font.render("Quit Game", True, self.quit_button_color)

        self.continue_rect.center = self.screen_rect.center

        self.game_pause_rect.center = self.screen_rect.center
        self.game_pause_rect.bottom = self.continue_rect.top
        self.game_pause_rect.y -= 50

        self.restart_rect.center = self.screen_rect.center
        self.restart_rect.y += self.continue_rect.height
        
        self.quit_rect.center = self.screen_rect.center
        self.quit_rect.y += self.restart_rect.height + 75

    def prep_died_menu(self):
        """Format menu for when player runs out of lives."""
        self.restart_button_image = self.settings.button_font.render("Restart Level", True, self.restart_button_color)
        self.quit_button_image = self.settings.button_font.render("Quit Game", True, self.quit_button_color)

        self.died_title_rect.center = self.screen_rect.center
        self.died_title_rect.y -= 100

        self.restart_rect.center = self.screen_rect.center
        self.restart_rect.top = self.died_title_rect.bottom

        self.quit_rect.center = self.screen_rect.center
        self.quit_rect.y += self.quit_rect.height

    def prep_you_won_menu(self):
        """Format menu for when player kills the boss."""
        self.restart_button_image = self.settings.button_font.render("Restart Level", True, self.restart_button_color)
        self.quit_button_image = self.settings.button_font.render("Quit Game", True, self.quit_button_color)

        self.you_won_rect.center = self.screen_rect.center
        self.you_won_rect.y -= 100

        self.restart_rect.center = self.screen_rect.center
        self.restart_rect.top = self.you_won_rect.bottom

        self.quit_rect.center = self.screen_rect.center
        self.quit_rect.y += self.quit_rect.height

    def draw_main_menu(self):
        """Draw the main menu to the screen."""
        self.prep_main_menu()
        self.screen.blit(self.game_title_image, self.game_title_rect)
        self.screen.blit(self.main_menu_image, self.main_menu_rect)
        self.screen.blit(self.play_button_image, self.play_rect)
        self.screen.blit(self.exit_button_image, self.exit_rect)
        
    def draw_pause_menu(self):
        """Draw the pause menu to the screen."""
        self.prep_pause_menu()
        self.screen.blit(self.game_pause_image, self.game_pause_rect)
        self.screen.blit(self.continue_button_image, self.continue_rect)
        self.screen.blit(self.restart_button_image, self.restart_rect)
        self.screen.blit(self.quit_button_image, self.quit_rect)
        
    def draw_died_menu(self):
        """Draw the 'Restart Game' button to the screen."""
        self.prep_died_menu()
        self.screen.blit(self.died_title_image, self.died_title_rect)
        self.screen.blit(self.restart_button_image, self.restart_rect)
        self.screen.blit(self.quit_button_image, self.quit_rect)

    def draw_you_won_menu(self):
        """Draw the 'You Won' menu to the screen."""
        self.prep_you_won_menu()
        self.screen.blit(self.you_won_title_image, self.you_won_rect)
        self.screen.blit(self.restart_button_image, self.restart_rect)
        self.screen.blit(self.quit_button_image, self.quit_rect)
