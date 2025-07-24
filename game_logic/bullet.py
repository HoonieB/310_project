import pygame as pg
from constants import Constants

class Bullet: 
    def __init__(self, x, y, width=5, height=10, bullet_speed=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bullet_speed =  bullet_speed
        self.bullet_rect = pg.Rect(x,y,width,height)

    def being_fired(self):
        # change the y position of the bullet
        self.y -= self.bullet_speed
        # update the bullet rect position to match the new y position 
        self.bullet_rect.y = self.y
        print(f"bullet being fired, y={self.y}")  

    def draw(self, screen):
        pg.draw.rect(screen, Constants.white, self.bullet_rect)

