import pygame
import sys
from time import sleep
from settings import Settings
from mario import Mario
from bowser import Bowser
from iceball import Iceball

class MarioGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.mario = Mario(self)
        self.bowser = Bowser(self)
        self.iceballs = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            self.mario.update()
            self._update_screen()
            self._update_iceballs()
            self._update_bowser()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()    
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_UP:
            self.mario.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.mario.moving_down = True
        elif event.key == pygame.K_RIGHT:
            self.mario.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.mario.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_iceball() 
        elif event.key == pygame.K_q:
            sys.exit()            

    def _check_keyup_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_UP:
            self.mario.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.mario.moving_down = False
        elif event.key == pygame.K_RIGHT:
            self.mario.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.mario.moving_left = False

    def _check_bowser_direction(self):
        if self.bowser.check_edges():
            self.settings.bowser_direction *= -1
           
    def _check_bowser_iceball_collisions(self):
        for iceball in self.iceballs.copy():
            if pygame.sprite.spritecollideany(self.bowser, self.iceballs):
                self.iceballs.remove(iceball)
                if self.settings.bowser_hp > 0:
                    self.settings.bowser_hp -= 1
                else:
                    sleep(1)
                    self.settings.bowser_hp = 8

    def fire_iceball(self):
        """Create a new iceball and add it to the iceballs group."""
        if len(self.iceballs) < self.settings.fireballs_allowed:
            new_iceball = Iceball(self)
            self.iceballs.add(new_iceball)

    def _update_iceballs(self):
        """Update the position of iceballs and get rid of old iceballs."""
        # Update iceball positions.
        self.iceballs.update()

        # Get rid of iceballs that have disappeared
        for iceball in self.iceballs.copy():
            if iceball.rect.left >= self.settings.screen_width:
                self.iceballs.remove(iceball)

        self._check_bowser_iceball_collisions()

    def _update_bowser(self):
        self._check_bowser_direction()
        self.bowser.update()
   

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.mario.blitme()
        self.bowser.blitme()
        self.iceballs.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = MarioGame()
    ai.run_game()
