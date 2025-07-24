import pygame as pg
from constants import Constants
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
        #print(f"before moving, x={self.x}, direction={direction}, screen_width={screen_width}")
        if direction == "left" and self.x > 0:
            self.x -= self.spaceship_speed
            #print(f"moving left, x={self.x},")
        elif direction == "right" and self.x < screen_width - self.width:
            self.x += self.spaceship_speed
            #print(f"moving right spaceship function is called, x={self.x}")

        self.spaceship_rect.x = self.x
        #print(f"after moving, x={self.x}, y={self.y}")

    def draw(self, screen):
        #print(f"drawing spaceship, x={self.x}, y={self.y}")
        screen.blit(self.spaceship_image, (self.x, self.y))

    def get_center(self):
        return (self.x + self.width // 2, self.y)

    def fire(self): 
        # inital x, y positions of the bullet 
        bullet_x = self.x + self.width // 2 
        bullet_y = self.y
        print("bullet created")
        return Bullet(bullet_x, bullet_y)