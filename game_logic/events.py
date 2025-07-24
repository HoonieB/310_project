import pygame as pg
from constants import Constants, GameState

#handle all events such as move, fire, start game, etc 
#BUTTON CLICK EVENTS
def handle_events(game_data, start_button=None):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_data.running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
           return event
        elif event.type == pg.KEYDOWN and game_data:
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