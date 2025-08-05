import pygame as pg
from constants import SoundEffects
from bullet import Bullet

class Spaceship:
    def __init__(self, x, y, width= 40, height =40, spaceship_speed=40):
        # spacceship horizontal position  
        self.x = x
        # spaceship vertical position 
        self.y = y
        # spaceship width(affect the width of the spaceship)
        self.width = width
        # spaceship height(affect the height of the spaceship)
        self.height = height
        # by default, the spaceship speed is 10, but increase or decrease it to make it faster of slower
        self.spaceship_speed = spaceship_speed
        # still need this recteangle for positioning of the spaceship and collision detection 
        self.spaceship_rect = pg.Rect(x, y, width, height)
        # spaceship image 
        self.spaceship_image = pg.image.load("game_assets/icons/space-invaders.png")
        self.spaceship_image = pg.transform.scale(self.spaceship_image, (self.width, self.height))

    def move(self, direction, screen_width):
        if direction == "left" and self.x > 0:
            self.x -= self.spaceship_speed
        elif direction == "right" and self.x < screen_width - self.width:
            self.x += self.spaceship_speed

        self.spaceship_rect.x = self.x

    def draw(self, screen):
        screen.blit(self.spaceship_image, (self.x, self.y))

    def get_center(self):
        return (self.x + self.width // 2, self.y)

    def fire(self): 
        # inital x, y positions of the bullet 
        bullet_x = self.x + self.width // 2 
        bullet_y = self.y
        SoundEffects.laser_sound.play()

        return Bullet(bullet_x, bullet_y)