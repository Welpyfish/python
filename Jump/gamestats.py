class GameStats:
    """Track statistics for Mario Game."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Start Mario Game in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.bowser_hp = self.settings.bowser_hp
        self.block_hp = self.settings.block_hp
