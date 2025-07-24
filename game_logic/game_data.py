from constants import Constants
from constants import GameState

# game data class to store game data such as score, lives, level, and running state
class GameData:
    def __init__(self):
        self.current_state = GameState.MENU
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.max_enemy_count = Constants.initial_enemy_count
        self.current_enemy_count = 0
        self.enemies_hit = 0
        self.running = True
        self.spaceship = None
        self.bullets = []
        self.enemies = []
        self.enemy_spawn_delay = 2000
    
    def reset_game(self):
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.enemy_count = Constants.initial_enemy_count
        self.spaceship = None 