import pygame
from pygame.sprite import Sprite

class Ground(Sprite):

    """A class to manage grounds fired from the ship"""

    def __init__(self, ai_game):
        """Create a ground object at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (self.settings.ground_color)

        # Create a ground rect 
        self.rect = pygame.Rect(0, 750, 1600, 50)

    def draw_ground(self):
        """Draw the ground to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

