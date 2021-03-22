import pygame
from random import randint
from block import Block 
from ground import Ground
from settings import Settings
from gamestats import GameStats
from bowser import Bowser
from fireball import Fireball
from iceball import Iceball

class Jump():
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.settings = Settings()
        self.stats = GameStats(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        self.block = Block(self)
        self.bowser = Bowser(self)
        self.ground = Ground(self)
        self.fireballs = pygame.sprite.Group()
        self.iceballs = pygame.sprite.Group()

        self.initSpeed = self.settings.initSpeed
        self.gravity = self.settings.gravity
        self.groundY = 0

    def run_game(self):
        """Start the main loop for the game."""
        self.block.y = self.ground.rect.top - self.block.rect.height - 1
        self.block.x = 5
        self.bowser.y = self.ground.rect.top - self.block.rect.height - 1
        while True:
            self._check_events()

            self.simulate_gravity()
            if self.block.isOnGround:
                self.block.simulate_friction(3)
            self.block.update()
            self._update_bowser()
            self._update_fireballs()
            self._update_iceballs()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()    
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.block.moving_right = True
        elif event.key == pygame.K_d:
            self.block.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.block.moving_left = True
        elif event.key == pygame.K_a:
            self.block.moving_left = True
        elif event.key == pygame.K_UP:
            self.jump() 
        elif event.key == pygame.K_w:
            self.jump() 
        elif event.key == pygame.K_SPACE:
            self.fire_iceball() 
        elif event.key == pygame.K_q:
            sys.exit()  

    def _check_keyup_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.block.moving_right = False
        elif event.key == pygame.K_d:
            self.block.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.block.moving_left = False
        elif event.key == pygame.K_a:
            self.block.moving_left = False 

    def simulate_gravity(self):
        self.block.speedY += self.gravity
        self.bowser.speedY += self.gravity
        self.block.y += self.block.speedY
        self.bowser.y += self.bowser.speedY
        if self.block.y > self.ground.rect.top - self.block.rect.height:
            self.block.speedY = 0
            self.block.y = self.ground.rect.top - self.block.rect.height
            self.block.isOnGround = True
        if self.bowser.y > self.ground.rect.top - self.bowser.rect.height:
            self.bowser.speedY = 0
            self.bowser.y = self.ground.rect.top - self.bowser.rect.height
            self.bowser.isOnGround = True

    def jump(self):
        if self.block.isOnGround:            
            self.block.y = self.ground.rect.top - self.block.rect.height - 1
            self.block.speedY -= self.initSpeed
            self.block.isOnGround = False

    def jump_bowser(self):
        if self.bowser.isOnGround:            
            self.bowser.y = self.ground.rect.top - self.bowser.rect.height - 1
            self.bowser.speedY -= self.initSpeed
            self.bowser.isOnGround = False

    def _check_bowser_collisions(self):
        for iceball in self.iceballs.copy():
            if pygame.sprite.spritecollideany(self.bowser, self.iceballs):
                self.iceballs.remove(iceball)
                if self.stats.bowser_hp > 0:
                    self.stats.bowser_hp -= 1
                else:
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)

    def _check_block_collisions(self):
        for fireball in self.fireballs.copy():
            if fireball.rect.colliderect(self.block.rect):
                self.fireballs.remove(fireball)
                if self.stats.block_hp > 0:
                    self.stats.block_hp -= 1
                else:
                    self.stats.game_active = False
                    pygame.mouse.set_visible(True)

    def _check_projectile_collisions(self):
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
        if len(self.iceballs) < self.settings.iceballs_allowed:
            new_iceball = Iceball(self)
            self.iceballs.add(new_iceball)

    def fire_fireball(self):
        """Create a new fireball and add it to the fireballs group."""
        if len(self.fireballs) < self.settings.fireballs_allowed:
            new_fireball = Fireball(self)
            self.fireballs.add(new_fireball)

    def _update_iceballs(self):
        """Update the position of iceballs and get rid of old iceballs."""
        # Update iceball positions.
        self.iceballs.update()

        # Get rid of iceballs that have disappeared
        for iceball in self.iceballs.copy():
            if iceball.rect.left >= self.settings.screen_width:
                self.iceballs.remove(iceball)

        self._check_bowser_collisions()

    def _update_fireballs(self):
        """Update the position of fireballs and get rid of old fireballs."""
        # Update fireball positions.
        self.fireballs.update()

        # Get rid of fireballs that have disappeared
        for fireball in self.fireballs.copy():
            if fireball.rect.right <= 0:
                self.fireballs.remove(fireball)

        self._check_block_collisions()
        self._check_projectile_collisions()

    def _update_bowser(self):
        self.bowser.update()
        if randint(1, 400) == 1:
            self.fire_fireball()
        if randint(1, 400) == 1:
            self.jump_bowser()
             
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.block.blitme()
        self.bowser.blitme()
        self.ground.draw_ground()
        self.fireballs.draw(self.screen)
        self.iceballs.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = Jump()
    ai.run_game()