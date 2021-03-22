import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    """A class to manage block."""

    def __init__(self, ai_game):
        """Initialize block and set its starting position."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the block image and get its rect
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/iceluigi.png")
        self.image = pygame.transform.scale(self.image, (65, 90))
        self.rect = self.image.get_rect()

        # Store a decimal value for the block's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.speedX = 0
        self.speedY = 0
        self.isOnGround = True

    def update(self):
        """Update block's position based on the movement flags."""
        # Update block's x and y values, not the rect
        if self.moving_right and self.speedX <= self.settings.maxspeed:
            if self.speedX < 0.05:
                self.speedX += 0.008
            elif 0.05 <= self.speedX < 0.1:
                self.speedX += 0.012
            else:
                self.speedX += 0.006
        if self.moving_left and self.speedX >= -self.settings.maxspeed:
            if self.speedX > -0.05:
                self.speedX -= 0.008
            elif -0.05 >= self.speedX > -0.1:
                self.speedX -= 0.012
            else:
                self.speedX -= 0.006
        self.simulate_friction(0.6)
        self.x += self.speedX
        self.check_edges()
        
        # Update rect block from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw block at his current location."""
        self.screen.blit(self.image, self.rect)

    def simulate_friction(self, number):
        if self.speedX > 0:
            self.speedX -= 0.001 * number
        elif self.speedX < 0:
            self.speedX += 0.001 * number

    def check_edges(self):
        if self.x > self.screen_rect.right - self.rect.width:
            self.x = self.screen_rect.right -self.rect.width
            self.speedX = 0
        elif self.x < 0:
            self.x = 0
            