import pygame as pg

from constants import Constants, GameState

# game data class to store game data such as score, lives, level, and running state
class GameData:
    def __init__(self):
        self.current_state = GameState.MENU
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.running = True
        self.spaceship = None
        self.bullets = [] 
        self.enemies = []
        self.base_enemy_speed = Constants.initial_enemy_speed
        self.enemy_spawn_delay = Constants.initial_enemy_spawn_delay
        self.score_for_next_level = Constants.initial_score_for_next_level 
        # initilaizd to a number bigger than cooldown so, in the event_handling, current - last_shot_time is greater than bullet_cooldown
        self.last_shot_time = -4000
        # bullet delay is 1 second for now, will be changed later
        self.bullet_cooldown = 1000
        self.last_enemy_spawn_time = pg.time.get_ticks()
        
    def is_game_over(self):
        return self.lives <= 0 
    
    def reset_game(self):
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.spaceship = None 
        self.enemy_spawn_delay = Constants.initial_enemy_spawn_delay
        self.base_enemy_speed = Constants.initial_enemy_speed
        self.last_shot_time = -4000
        self.bullets.clear()
        self.enemies.clear()
        self.last_enemy_spawn_time = pg.time.get_ticks()
    
        # level up, increase eneemy speed and decrease enemy spawn delay(appear faster )
    def level_up(self):
        # level increases
        self.level += 1
        # enemy moves faster 
        self.base_enemy_speed += 0.1
        # change the speed of enemy already displayed on the screen, if we want to change the speed of newly created enemy only, just delete the for loop 
        for enemy in self.enemies:
            enemy.enemy_speed = self.base_enemy_speed
        # enemy spawns faster 
        self.enemy_spawn_delay = max(300, self.enemy_spawn_delay - 300)
        print(f"Level Up! Current Level: {self.level}, Enemy Speed: {self.base_enemy_speed:.2f}, Spawn Delay: {self.enemy_spawn_delay}ms")