import pygame
import sys
from time import sleep
from random import randint
from settings import Settings
from gamestats import GameStats
from mario import Mario
from bowser import Bowser
from iceball import Iceball
from fireball import Fireball

class MarioGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.mario = Mario(self)
        self.bowser = Bowser(self)
        self.iceballs = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            self.mario.update()
            self._update_screen()
            self._update_iceballs()
            self._update_fireballs()
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
                if self.stats.bowser_hp > 0:
                    self.stats.bowser_hp -= 1
                else:
                    sleep(1)
                    self.stats.bowser_hp = self.settings.bowser_hp

    def _check_mario_fireball_collisions(self):
        for fireball in self.fireballs.copy():
            if pygame.sprite.spritecollideany(self.mario, self.fireballs):
                self.fireballs.remove(fireball)
                if self.settings.mario_hp > 0:
                    self.settings.mario_hp -= 1
                else:
                    sleep(1)
                    self.settings.mario_hp = 8

    def _check_iceball_fireball_collisions(self):
        for fireball in self.fireballs.copy():
            if pygame.sprite.spritecollideany(fireball, self.iceballs):
                if fireball.fireball_hp > 0:
                    fireball.fireball_hp -= 1
                    pygame.sprite.groupcollide(self.iceballs, self.fireballs, True, False)
                    fireball.image = pygame.transform.scale(fireball.image, (60, 45))
                else:
                    pygame.sprite.groupcollide(self.iceballs, self.fireballs, True, True)
            

    def fire_iceball(self):
        """Create a new iceball and add it to the iceballs group."""
        if len(self.iceballs) < self.settings.fireballs_allowed:
            new_iceball = Iceball(self)
            self.iceballs.add(new_iceball)

    def fire_fireball(self):
        """Create a new fireball and add it to the fireballs group."""
        new_fireball = Fireball(self)
        self.fireballs.add(new_fireball)

    def generate_fireball_chance(self):
        if -120 <= self.bowser.y - self.mario.y <= 120:
            self.fireball_chance = self.settings.fireball_chance
            print("lucky")
        else: 
            self.fireball_chance = 0

    def _update_iceballs(self):
        """Update the position of iceballs and get rid of old iceballs."""
        # Update iceball positions.
        self.iceballs.update()

        # Get rid of iceballs that have disappeared
        for iceball in self.iceballs.copy():
            if iceball.rect.left >= self.settings.screen_width:
                self.iceballs.remove(iceball)

        self._check_bowser_iceball_collisions()

    def _update_fireballs(self):
        """Update the position of fireballs and get rid of old fireballs."""
        # Update fireball positions.
        self.fireballs.update()

        # Get rid of fireballs that have disappeared
        for fireball in self.fireballs.copy():
            if fireball.rect.right <= 0:
                self.fireballs.remove(fireball)

        self._check_mario_fireball_collisions()
        self._check_iceball_fireball_collisions()

    def _update_bowser(self):
        self._check_bowser_direction()
        self.bowser.update()
        self.generate_fireball_chance()
        if randint(1, 500 - self.fireball_chance) == 1:
            self.fire_fireball()
   
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.mario.blitme()
        self.bowser.blitme()
        self.iceballs.draw(self.screen)
        self.fireballs.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = MarioGame()
    ai.run_game()
