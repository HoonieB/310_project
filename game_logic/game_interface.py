import pygame as pg
import random
from constants import Constants
from constants import GameState
from game_settings import GameSettings
from game_data import GameData
from spaceship import Spaceship
from enemy import Enemy
from draw_game import *
from events import handle_events

# main game loop 
def main():
    # Initialize pygame
    pg.init()
    
    # Create game objects
    settings = GameSettings()
    game_data = GameData()
    
    # Initialize display
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    font = pg.font.Font(None, settings.font_size)
    last_enemy_spawn_time = pg.time.get_ticks()
    collision_sound = pg.mixer.Sound("game_assets/sound/small-explosion-103931.mp3")
    
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
                    ship_y = Constants.window_height - 40
                    # create a new spaceship object
                    game_data.spaceship = Spaceship(ship_x, ship_y) # type: ignore
                    game_data.current_state = GameState.PLAYING
                    if game_data.spaceship:
                        print("spaceship is created!")
                    else: 
                        print("No spaceship created!")

        elif game_data.current_state == GameState.PLAYING:
            draw_game(screen, game_data)
            
            if game_data.spaceship:
                game_data.spaceship.draw(screen)

            for bullet in game_data.bullets:
                # makes the new bullet 
                bullet.being_fired()
                # draw the bullet on the screen 
                bullet.draw(screen)
                # if the bullet is out of the screen, remove it from the list 
                if bullet.y < 0:
                    game_data.bullets.remove(bullet)
            
            current_time = pg.time.get_ticks()
            if current_time - last_enemy_spawn_time > game_data.enemy_spawn_delay and game_data.current_enemy_count < game_data.max_enemy_count:
                # the 40 is the width of the enemy, change it accordingly as the enemy width changes
                new_enemy = Enemy(random.randint(0, Constants.window_width - 40), 0)
                game_data.current_enemy_count += 1
                game_data.enemies.append(new_enemy)
                last_enemy_spawn_time = current_time 

            #if current wave finished, start new one
            if game_data.enemies_hit == game_data.max_enemy_count:
                #adjust difficulty
                game_data.level += 1
                game_data.max_enemy_count += 5
                if (game_data.enemy_spawn_delay > 50):
                    game_data.enemy_spawn_delay = game_data.enemy_spawn_delay - 100
                
                #clear game data
                #game_data.enemies_hit = 0
                game_data.enemies.clear()
            
            for bullet in game_data.bullets[:]:
                for enemy in game_data.enemies[:]:
                    if bullet.bullet_rect.colliderect(enemy.enemy_rect):
                        game_data.bullets.remove(bullet)
                        game_data.enemies.remove(enemy)
                        game_data.score += 1 
                        game_data.enemies_hit += 1
                        break
            for enemy in game_data.enemies[:]:
                if enemy.enemy_rect.colliderect(game_data.spaceship.spaceship_rect):
                    collision_sound.play()
                    game_data.lives -= 1
                    game_data.enemies_hit += 1
                    game_data.enemies.remove(enemy)
                    break

            for enemy in game_data.enemies[:]:
                enemy.move()
                enemy.draw(screen)

                if enemy.y + enemy.height >= Constants.window_height:
                    game_data.current_state = GameState.GAME_OVER


            
    
        elif game_data.current_state == GameState.GAME_OVER:
            draw_game_over(screen, font, game_data)
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()



if __name__ == "__main__":
    main()


