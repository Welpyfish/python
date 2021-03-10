import pygame
from pygame.sprite import Sprite

class Bowser(Sprite):
    """A class to manage bowser."""

    def __init__(self, ai_game):
        """Initialize bowser and set his starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # Load the bowser image and set its rect attribute.
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/bowser.png")
        self.image = pygame.transform.scale(self.image, (120, 144))
        self.rect = self.image.get_rect()

        # Start bowser near the middle right of the screen.
        self.rect.midright = self.screen_rect.midright

        # Store bowser's exact vertical position.
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if bowser is at edge of the screen."""
        if self.rect.bottom >= self.screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        """Move bowser up or down."""
        self.y += (self.settings.bowser_speed * self.settings.bowser_direction)
        self.rect.y = self.y

    def blitme(self):
        """Draw bowser at his current location."""
        self.screen.blit(self.image, self.rect)

    def center_bowser(self):
        """Center bowser on the screen."""
        self.rect.midright = self.screen_rect.midright
        self.y = float(self.rect.y)

    