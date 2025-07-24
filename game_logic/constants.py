from enum import Enum

# Game state enum class to store the game state 
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

# constant class to store all the constants for the game 
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
    initial_lives = 1
    initial_score = 0
    initial_level = 0
    initial_enemy_count = 5