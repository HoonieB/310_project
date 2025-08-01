import sys
import os

import pygame as pg
import random
from constants import Constants
from constants import GameState
from game_settings import GameSettings
from game_data import GameData
from enemy import Enemy
from draw_game import *
from events import handle_game_events, handle_menu_events, handle_game_over_events
import mediapipe as mp
from collections import deque, Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from knn_model import KNN, load_dataset
import numpy as np
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# main game loop 
def main():

    features, labels = load_dataset("dataset.csv")
    knn_model = KNN(k=5)
    knn_model.fit(features, labels)

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
    
    capture = cv2.VideoCapture(0)
    
    history = deque(maxlen=7)
    MIN_GESTURE_COUNT = 4

    # Main game loop
    while game_data.running:
        # Menu
        if (game_data.current_state == GameState.MENU):
            start_button = draw_menu(screen, font, settings)
            for event in pg.event.get():
                handle_menu_events(game_data, event, start_button)
                
        # Playing
        elif game_data.current_state == GameState.PLAYING:

            ret, frame = capture.read()
            if not ret:
                continue
            
            flipped_frame = cv2.flip(frame, 1)  # to mirror the camera feed

            rgb_image = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)  # change from OpenCV colour format to RGB

            result = hands.process(rgb_image)

            if result.multi_hand_landmarks:
                hand_landmarks = result.multi_hand_landmarks[0]

                landmark_points = []
                for lm in hand_landmarks.landmark:
                    landmark_points.extend([lm.x, lm.y, lm.z])
                landmark_points = np.array(landmark_points).reshape(1, -1)
                
                predicted = knn_model.predict(landmark_points)[0]
                history.append(predicted)
                #this turns the list of values into a numpy array

                gesture_counts = Counter(history)
                most_common = gesture_counts.most_common(1)

                if most_common and most_common[0][1] >= MIN_GESTURE_COUNT:
                    smoothed_prediction = most_common[0][0]

                    print(f"Gesture: {smoothed_prediction}", True, Constants.white)

                    knuckle1 = hand_landmarks.landmark[5]
                    knuckle2 = hand_landmarks.landmark[9]
                    knuckle3 = hand_landmarks.landmark[13]
                    knuckle4 = hand_landmarks.landmark[17]
                    coords = [knuckle1.x, knuckle2.x, knuckle3.x, knuckle4.x]
                    x_coordinate1 = np.mean(coords)
                    x_pixel = int(x_coordinate1 * Constants.window_width)

                    game_data.spaceship.x = x_pixel

                
                    handle_game_events(game_data, smoothed_prediction)
                else:
                    handle_game_events(game_data, None)
                
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
                    if game_data.lives == 0:
                        game_data.current_state = GameState.GAME_OVER
                    break

            for enemy in game_data.enemies[:]:
                enemy.move()
                enemy.draw(screen)

                if enemy.y + enemy.height >= Constants.window_height:
                    game_data.current_state = GameState.GAME_OVER
    
        # Game Over
        elif game_data.current_state == GameState.GAME_OVER:
            draw_game_over(screen, font, game_data)
            for event in pg.event.get():
                handle_game_over_events(game_data, event)
        
        # Update display
        pg.display.flip()
    
    # end the game 
    pg.quit()
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


