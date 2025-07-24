import pygame as pg

class Enemy:
    def __init__(self, x, y, width=40, height=40, enemy_speed=0.3, spawn_delay=2000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enemy_speed = enemy_speed
        self.enemy_rect = pg.Rect(x,y,width,height)
        self.enemy_image = pg.image.load("game_assets/icons/enemy.png")
        self.enemy_image = pg.transform.scale(self.enemy_image, (self.width, self.height))
        self.spawn_delay = spawn_delay
   
    def move(self):
        self.y += self.enemy_speed
        self.enemy_rect.y = self.y
    
    def draw(self, screen):
        #print(f"drawing enemy, x={self.x}, y={self.y}")
        screen.blit(self.enemy_image, (self.x, self.y))

