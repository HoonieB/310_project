import pygame as pg
from constants import Constants, GameState
from spaceship import Spaceship

#handle active events such as move, fire, start game, etc 
def handle_game_events(game_data, event):
    if event.type == pg.KEYDOWN and game_data:
        if event.key == pg.K_LEFT and game_data.spaceship:
            game_data.spaceship.move("left", Constants.window_width) # type: ignore
            print("moving left")
        elif event.key == pg.K_RIGHT and game_data.spaceship:
            game_data.spaceship.move("right", Constants.window_width) # type: ignore
            print("moving right")
        elif event.key == pg.K_SPACE and game_data.spaceship:
            print("firing bullet, space bar is pressed")
            # create a a new bullet objet 
            bullet = game_data.spaceship.fire()
            # added to the bulelt list 
            game_data.bullets.append(bullet)
    return None

#handle menu events
def handle_menu_events(game_data, event, start_button):
    if event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        if start_button.is_clicked(mouse_pos):
            print("Game started!") 
            ship_x = (Constants.window_width // 2)
            ship_y = Constants.window_height - 40
            # create a new spaceship object
            game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
            game_data.current_state = GameState.PLAYING
            if game_data.spaceship:
                print("spaceship is created!")
            else: 
                print("No spaceship created!")
    return None
                
def handle_game_over_events(game_data, event):
    if event.type == pg.QUIT:
        game_data.running = False
    return None