import pygame as pg
from enum import Enum
import mediapipe as mp
import cv2


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils



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
    initial_lives = 5
    initial_score = 0
    initial_level = 0

# Game state enum class to store the game state 
class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"


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



# game data class to store game data such as score, lives, level, and running state
class GameData:
    def __init__(self):
        self.current_state = GameState.MENU
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.running = True
        self.spaceship = None
    
    def is_game_over(self):
        return self.lives <= 0
    
    def reset_game(self):
        self.score = Constants.initial_score
        self.lives = Constants.initial_lives
        self.level = Constants.initial_level
        self.spaceship = None 


# button class to create a button object
class Button:
    def __init__(self, x, y, width, height, button_text_content, font_size, color=Constants.navy):
        self.rect = pg.Rect(x, y, width, height)
        self.text = button_text_content
        self.font = font_size
        self.color = color
        self.text_surface = None
        self.text_rect = None
        self._create_text()
    
    # create text surface and position it on button 
    def _create_text(self):
        self.text_surface = self.font.render(self.text, True, Constants.white)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
    
    # draw button and text on screen 
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    
    # check if button was clicked
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Spaceship:
    def __init__(self, x, y, width= 40, height =40, speed=10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pg.Rect(x, y, width, height)

    def move(self, coordinate, screen_width):
        #print(f"before moving, x={self.x}, direction={direction}, screen_width={screen_width}")

        self.x = coordinate * screen_width
        self.rect.x = self.x
       # print(f"after moving, x={self.x}, y={self.y}")

    def draw(self, screen, colour):
        #print(f"drawing spaceship, x={self.x}, y={self.y}")
        pg.draw.rect(screen, colour, self.rect)

    def get_center(self):
        return (self.x + self.width // 2, self.y)

    def fire(self): 
        return None 



# draw the menu screen and return the start button 
def draw_menu(screen, font, settings):
    # initialize the screen with black color 
    screen.fill(Constants.black)
    
    # Create and draw start button
    start_button = Button(
        settings.center_x, 
        settings.center_y, 
        settings.button_width, 
        settings.button_height, 
        "Start Game", 
        font
    )
    start_button.draw(screen)
    
    return start_button

# draw the game screen, COME BACK TO THIS LATER AND FIX THE RESPONSIVENESS OF THE UI
def draw_game(screen, game_data):
    screen.fill(Constants.black)

    # I will make the game UI here and the logic as well, align the labels properly!!!, will fix it later, leaving it like this for now for demo purpose
    # create different fonts for different labels 
    score_font = pg.font.Font(None, Constants.game_text_font_size)
    lives_font = pg.font.Font(None, Constants.game_text_font_size)
    level_font = pg.font.Font(None, Constants.game_text_font_size)

    # draw score label at the top left corner of the screen 
    score_label = score_font.render(f"Score: {game_data.score}", True, Constants.white)
    screen.blit(score_label, (10, 10))

    # draw lives label at the top right corner of the screen
    lives_label = lives_font.render(f"Lives: {game_data.lives}", True, Constants.white)
    screen.blit(lives_label, (Constants.window_width - 90, 10))

    # draw level label at the top center of the screen 
    level_label = level_font.render(f"Level: {game_data.level}", True, Constants.white)
    screen.blit(level_label, (Constants.window_width//2 - 50, 10))
 


# draw the game over screen 
def draw_game_over(screen, font, game_data):
    screen.fill(Constants.black)
    game_over_text = font.render("Game Over!", True, Constants.white)
    text_rect = game_over_text.get_rect(center=(Constants.window_width//2 , Constants.window_height//2))
    screen.blit(game_over_text, text_rect)


# handel all events such as move, fire, start game, etc 
def handle_events(game_data):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_data.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            return event 
        #elif event.type == pg.KEYDOWN:
            #if event.key == pg.K_LEFT and game_data.spaceship:
               # game_data.spaceship.move(coordinate, Constants.window_width) # type: ignore
                #print("mmovign left ")
            #elif event.key == pg.K_RIGHT and game_data.spaceship:
              #  game_data.spaceship.move(coordinate, Constants.window_width) # type: ignore
                #print("moving right")
        
            # rn the click event for button handling
    return None

# main game loop 
def main():
    # Initialize pygame
    pg.init()
    settings = GameSettings()
    game_data = GameData()
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    font = pg.font.Font(None, settings.font_size)

    capture = cv2.VideoCapture(0)
    
    # Main game loop
    while game_data.running:
        # Handle events
        click_event = handle_events(game_data)
        
        # Update game state
        if game_data.is_game_over():
            game_data.current_state = GameState.GAME_OVER
        
        # Draw current screen and handle interactions
        if game_data.current_state == GameState.MENU:
            start_button = draw_menu(screen, font, settings)
            
            # Handle button clicks
            if click_event and click_event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    print("Game started!") 
                    ship_x = (Constants.window_width // 2)
                    ship_y = Constants.window_height - 30
                    game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
                    game_data.current_state = GameState.PLAYING
                    draw_game(screen, game_data)


        elif game_data.current_state == GameState.PLAYING:
            screen.fill(Constants.black)

            ret, frame = capture.read()
            if not ret:
                continue

            flipped_frame = cv2.flip(frame, 1)  # to mirror the camera feed

            rgb_image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)  # change from OpenCV colour format to RGB

            result = hands.process(rgb_image)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]
                knuckle1 = hand_landmarks.landmark[14]
                x_coordinate1 = knuckle1.x
                x_pixel = int(x_coordinate1 * Constants.window_width)

                x_pixels = max(0, min(Constants.window_width - game_data.spaceship.width, x_pixel))
                game_data.spaceship.x = x_pixels
                game_data.spaceship.rect.x = x_pixels

                pg.draw.rect(screen, Constants.white, game_data.spaceship.rect)

            # draw_game(screen, game_data)
            game_data.spaceship.draw(screen, Constants.white)

        elif game_data.current_state == GameState.GAME_OVER:
            draw_game_over(screen, font, game_data)


        pg.display.flip()
    # end the game 
    pg.quit()

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


