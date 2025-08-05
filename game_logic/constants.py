import pygame as pg
from enum import Enum

class Constants:
    # Window size setting 
    window_width = 540
    window_height = 540

    # Button size setting 
    button_width = 200
    button_height = 100
    button_font = 50  # Font sizes for different text elements
    button_font_size = 36
    game_text_font_size = 28
    # Colors codes (RGB values)
    white = (255, 255, 255)
    navy = (25, 25, 112)
    black = (0, 0, 0)

    # Game values settings
    initial_lives = 5
    initial_score = 0
    initial_level = 1

    # will be changed as game difficulty changes 
    initial_enemy_speed = 2
    initial_enemy_spawn_delay = 2000
    initial_score_for_next_level = 10
    
# Game States
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    
class SoundEffects():
    laser_sound = pg.mixer.Sound("game_assets/sound/laser-312360.wav")
    collision_sound = pg.mixer.Sound("game_assets/sound/small-explosion-103931.mp3")
    game_start_sound = pg.mixer.Sound("game_assets/sound/gamestart-272829.mp3")
    game_over_sound = pg.mixer.Sound("game_assets/sound/game-over-38511.mp3")
    enemy_being_hit = pg.mixer.Sound("game_assets/sound/arcade-ui-14-229514.mp3")   