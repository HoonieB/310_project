import pygame as pg
from constants import Constants
from button import Button

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