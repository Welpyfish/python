class Settings:
    """ A class to store all settings"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1600
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ground_color = (0, 50, 0)

        # Mario settings
        self.maxspeed = 1
        self.block_initSpeed = 3
        self.gravity = 0.02
        self.mario_right_speed = 0
        self.mario_left_speed = 0

        # Bowser settings
        self.bowser_speed = 1
        self.jump_chance = 600
        self.bowser_initSpeed = 3

        # Fireball settings
        self.fireball_speed = 1
        self.fireballs_allowed = 12
        self.fireball_chance = 200

        # Iceball settings
        self.iceball_speed = 1.5
        self.iceballs_allowed = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""

        self.bowser_hp = 32

        self.block_hp = 5
        self.fireball_hp = 1
