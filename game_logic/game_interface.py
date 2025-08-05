import pygame as pg
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from collections import deque, Counter
import mediapipe as mp

pg.init()
pg.mixer.init()

#Game components
from constants import *
from draw import *
from game_settings import GameSettings
from game_data import GameData
from events import *
from enemy import Enemy

from game_assets.knn_model import KNN, load_dataset

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# main game loop 
def main():
    # initialize pygame
    pg.init()

    # import knn model
    features, labels = load_dataset("dataset.csv")
    knn_model = KNN(k=5)
    knn_model.fit(features, labels)
    
    settings = GameSettings()
    game_data = GameData()

    # initialize display
    screen = pg.display.set_mode((settings.screen_width, settings.screen_height))
    font = pg.font.Font(None, settings.font_size)

    capture = cv2.VideoCapture(0)
    gesture_history = deque(maxlen=7)
    MIN_GESTURE_COUNT = 4
    
    # main game loop
    while game_data.running:
         # menu
        if (game_data.current_state == GameState.MENU):
            start_button = draw_menu(screen, font, settings)
            for event in pg.event.get():
                handle_menu_events(game_data, event, start_button)

        # game logic, firing bullets, enemy spaceship collision, enemy spawn, enemy being killed by the bullet
        elif game_data.current_state == GameState.PLAYING:

            ret, frame = capture.read()
            if ret:
                flipped = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
                result = hands.process(rgb)

                if result.multi_hand_landmarks:
                    landmarks = result.multi_hand_landmarks[0]

                    lm_vector = []
                    for lm in landmarks.landmark:
                        lm_vector.extend([lm.x, lm.y, lm.z])
                    lm_vector = np.array(lm_vector).reshape(1, -1)

                    pred = knn_model.predict(lm_vector)[0]
                    gesture_history.append(pred)

                    gesture_counts = Counter(gesture_history)
                    most_common = gesture_counts.most_common(1)

                    if most_common and most_common[0][1] >= MIN_GESTURE_COUNT:
                        smoothed = most_common[0][0]
                        print("Gesture:", smoothed)

                        # move spaceship via real life hand movement
                        knuckles = [landmarks.landmark[i].x for i in [5, 9, 13, 17]]
                        avg_x = np.mean(knuckles)
                        game_data.spaceship.x = int(avg_x * Constants.window_width)

                        # trigger events (e.g., fire gun)
                        handle_game_events(game_data, smoothed)
                    else:
                        handle_game_events(game_data, None)


            draw_game(screen, game_data)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_data.running = False
            
            # draw the spaceship on the screen 
            if game_data.spaceship:
                game_data.spaceship.draw(screen)
            
            # game difficulty adjustment happens here 
            if game_data.score >= game_data.score_for_next_level:
                game_data.level_up()
                game_data.score_for_next_level += 10 

            # draw the bullets on the screen 
            for bullet in game_data.bullets:
                # makes the new bullet 
                bullet.being_fired()
                # draw the bullet on the screen 
                bullet.draw(screen)
                # if the bullet is out of the screen, remove it 
                if bullet.y < 0:
                    game_data.bullets.remove(bullet)
            
            # enemy spawning 
            current_time_for_enemy_respawing = pg.time.get_ticks()
            if current_time_for_enemy_respawing - game_data.last_enemy_spawn_time > game_data.enemy_spawn_delay:
                # the 40 is the width of the enemy, change it accordingly as the enemy width changes
                new_enemy = Enemy(random.randint(0, Constants.window_width - 40), 0, enemy_speed=game_data.base_enemy_speed)
                # print(f"new_enemy created, speed:{new_enemy.enemy_speed}, {game_data.last_enemy_spawn_time}")
                # add the new eneemy to the enemy list 
                game_data.enemies.append(new_enemy)
                # update the last_enemy_spawn_time to current time 
                game_data.last_enemy_spawn_time = current_time_for_enemy_respawing 
            
            # enemy-bullet colllision detection, [:] is a list comprehension to iterate over a copy of the list
            for bullet in game_data.bullets[:]:
                for enemy in game_data.enemies[:]:
                    if bullet.bullet_rect.colliderect(enemy.enemy_rect):
                        SoundEffects.enemy_being_hit.play()
                        game_data.bullets.remove(bullet)
                        game_data.enemies.remove(enemy)
                        game_data.score += 1 
                        break
                    
            # enemy-spaceship collision detection 
            for enemy in game_data.enemies[:]:
                if enemy.enemy_rect.colliderect(game_data.spaceship.spaceship_rect):
                    SoundEffects.collision_sound.play()
                    game_data.lives -= 1
                    game_data.enemies.remove(enemy)
                    break


            # enemy movement
            for enemy in game_data.enemies[:]:
                enemy.move()
                enemy.draw(screen)
                # print(f"new_enemy drawn, speed:{new_enemy.enemy_speed}, {game_data.last_enemy_spawn_time}")
                # enemy hits the bottom of the screen? game over 
                if enemy.y + enemy.height >= Constants.window_height:
                    game_data.current_state = GameState.GAME_OVER
                    SoundEffects.game_over_sound.play()


        elif game_data.current_state == GameState.GAME_OVER:
            game_over_menu_button = draw_game_over(screen, font, game_data, settings)
            for event in pg.event.get():
                handle_game_over_events(game_data, event, game_over_menu_button)
                    
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()


