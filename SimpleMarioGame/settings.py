class Settings:
    """ A class to store all settings for MarioGame"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Mario settings
        self.mario_up_speed = 2
        self.mario_down_speed = 2
        self.mario_right_speed = 2
        self.mario_left_speed = 2

        # Bowser settings
        self.bowser_speed = 1

        # Fireball settings
        self.fireball_speed = 1.5
        self.fireballs_allowed = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""

        # bowser_direction of 1 represents down; -1 represents up
        self.bowser_direction = -1
        self.bowser_hp = 16



        