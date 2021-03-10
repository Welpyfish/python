import pygame
from pygame.sprite import Sprite

class Fireball(Sprite):
    """A class to manage fireballs fired from Bowser"""

    def __init__(self, ai_game):
        """Create an fireball object"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the fireball image and get its rect
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/fireball.png")
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()

        self.rect.midright = ai_game.bowser.rect.midleft

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

        self.fireball_hp = self.settings.fireball_hp

    def update(self):
        """Move the fireball up the screen."""
        # Update the decimal position of the bullet.
        self.x -= self.settings.fireball_speed
        # Update the rect position
        self.rect.x = self.x

