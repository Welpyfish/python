import pygame
from pygame.sprite import Sprite

class Iceball(Sprite):
    """A class to manage iceballs fired from Mario"""

    def __init__(self, ai_game):
        """Create an iceball object"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the iceball image and get its rect
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/iceball.png")
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()

        self.rect.midleft = ai_game.mario.rect.midright

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the iceball up the screen."""
        # Update the decimal position of the bullet.
        self.x += self.settings.iceball_speed
        # Update the rect position
        self.rect.x = self.x


