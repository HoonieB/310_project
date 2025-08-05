import pygame as pg
from constants import Constants, GameState, SoundEffects
from spaceship import Spaceship

#handle active events such as move, fire, start game, etc 
def handle_game_events(game_data, gesture):
    if gesture is None:
        return
    if gesture == "gun" and game_data.spaceship:
        current_time_for_bullet_charging = pg.time.get_ticks()
        if current_time_for_bullet_charging - game_data.last_shot_time > game_data.bullet_cooldown:
            bullet = game_data.spaceship.fire()
            game_data.bullets.append(bullet)
            game_data.last_shot_time = current_time_for_bullet_charging
            
#handle menu events
def handle_menu_events(game_data, event, button):
    if event.type == pg.QUIT:
        game_data.running = False
    elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        if button.is_clicked(mouse_pos):
            print("Game started!") 
            ship_x = (Constants.window_width // 2)
            ship_y = Constants.window_height - 40
            # create a new spaceship object
            game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
            game_data.current_state = GameState.PLAYING
            SoundEffects.game_start_sound.play()
                
def handle_game_over_events(game_data, event, button):
    if event.type == pg.QUIT:
        game_data.running = False
    elif event.type == pg.MOUSEBUTTONDOWN:
        mouse_pos = pg.mouse.get_pos()
        if button.is_clicked(mouse_pos):
            game_data.reset_game()
            game_data.current_state = GameState.MENU