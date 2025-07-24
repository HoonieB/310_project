from constants import Constants

# Game settings class to store game settings
class GameSettings:
    def __init__(self):
        self.screen_width = Constants.window_width
        self.screen_height = Constants.window_height
        self.button_width = Constants.button_width
        self.button_height = Constants.button_height
        self.font_size = Constants.game_text_font_size
        
        # Calculate center coordinates once
        self.center_x = self.screen_width // 2 - self.button_width // 2
        self.center_y = self.screen_height // 2 - self.button_height // 2