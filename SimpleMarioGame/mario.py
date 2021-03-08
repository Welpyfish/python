import pygame

class Mario:
    """A class to manage mario."""

    def __init__(self, ai_game):
        """Initialize mario and set his starting position."""

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect
        self.image = pygame.image.load("C:/William/git/python/SimpleMarioGame/images/iceluigi.png")
        self.image = pygame.transform.scale(self.image, (65, 90))
        self.rect = self.image.get_rect()
    
        # Start each new mario at the center left of the screen.
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update mario's position based on the movement flags."""
        # Update mario's x and y values, not the rect
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.mario_up_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mario_down_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mario_right_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.mario_left_speed

        # Update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw mario at his current location."""
        self.screen.blit(self.image, self.rect)
