import pygame
from random import randint
from block import Block 
from ground import Ground
from axe import Axe
from settings import Settings
from gamestats import GameStats
from button import Button
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
        
        # Fullscreen mode
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width 
        #self.settings.screen_height = self.screen.get_rect().height
        
        self.block = Block(self)
        self.bowser = Bowser(self)
        self.ground = Ground(self)
        self.axe = Axe(self)
        self.fireballs = pygame.sprite.Group()
        self.iceballs = pygame.sprite.Group()

        self.gravity = self.settings.gravity
        self.groundY = 0

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        self.block.y = self.ground.rect.top - self.block.rect.height - 1
        self.block.x = 5
        self.bowser.y = self.ground.rect.top - self.bowser.rect.height - 1
        self.bowser.x = self.settings.screen_width - self.axe.rect.width - self.bowser.rect.width - 105
        self.axe.rect.x = self.settings.screen_width - self.axe.rect.width
        self.axe.rect.y = self.ground.rect.top - self.axe.rect.height

        while True:
            self._check_events()

            if self.stats.game_active:
                self.simulate_gravity()
                if self.block.isOnGround:
                    self.block.simulate_friction(3)
                self.block.update()
                self._update_bowser()
                self._update_fireballs()
                self._update_iceballs()
            
            self._update_screen()

    def _start_game(self):

        self.block.y = self.ground.rect.top - self.block.rect.height - 1
        self.block.x = 5
        self.speedX = 0
        self.speedY = 0
        self.bowser.y = self.ground.rect.top - self.bowser.rect.height - 1
        self.bowser.x = self.settings.screen_width - self.axe.rect.width - self.bowser.rect.width - 105
        self.axe.rect.x = self.settings.screen_width - self.axe.rect.width
        self.axe.rect.y = self.ground.rect.top - self.axe.rect.height

        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets
        self.iceballs.empty()
        self.fireballs.empty()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

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
                self._check_play_button(mouse_pos)
                
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
        elif event.key == pygame.K_p:
            self._start_game()  
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

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def win(self):
        self.win_button = Button(self, "Win")
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

    def lose(self):
        self.win_button = Button(self, "Lose")
        self.stats.game_active = False
        pygame.mouse.set_visible(True)

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
            self.block.speedY -= self.settings.block_initSpeed
            self.block.isOnGround = False

    def jump_bowser(self):
        if self.bowser.isOnGround:            
            self.bowser.y = self.ground.rect.top - self.bowser.rect.height - 1
            self.bowser.speedY -= self.settings.bowser_initSpeed
            self.bowser.isOnGround = False

    def _check_bowser_collisions(self):
        for iceball in self.iceballs.copy():
            if pygame.sprite.spritecollideany(self.bowser, self.iceballs):
                self.iceballs.remove(iceball)
                if self.stats.bowser_hp > 0:
                    self.stats.bowser_hp -= 1
                else:
                    self.win()

        if self.bowser.rect.colliderect(self.block.rect) and self.block.speedX > -0.5:
            self.block.speedX -= 0.5
            if self.stats.block_hp > 0:
                self.stats.block_hp -= 0.2
            else:
                self.lose()

    def _check_block_collisions(self):
        for fireball in self.fireballs.copy():
            if fireball.rect.colliderect(self.block.rect):
                self.fireballs.remove(fireball)
                if self.stats.block_hp > 0:
                    self.stats.block_hp -= 1
                else:
                    self.lose()
        if self.block.rect.colliderect(self.axe.rect):
            self.win()

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
        #if randint
             
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.block.blitme()
        self.bowser.blitme()
        self.axe.blitme()
        self.ground.draw_ground()
        self.fireballs.draw(self.screen)
        self.iceballs.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = Jump()
    ai.run_game()