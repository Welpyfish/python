import pygame
from pygame.sprite import Sprite

class Axe(Sprite):

    """A class to manage grounds fired from the ship"""

    def __init__(self, ai_game):
        """Create a ground object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the bowser image and set its rect attribute.
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/Axe.png")
        self.image = pygame.transform.scale(self.image, (100, 130))
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw bowser at his current location."""
        self.screen.blit(self.image, self.rect)


