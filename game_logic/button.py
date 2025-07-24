import pygame as pg
from constants import Constants

# button class to create a button object
class Button:
    def __init__(self, x, y, width, height, button_text_content, font_size, color=Constants.navy):
        self.rect = pg.Rect(x, y, width, height)
        self.text = button_text_content
        self.font = font_size
        self.color = color
        self.text_surface = None
        self.text_rect = None
        self._create_text()
    
    # create text surface and position it on button 
    def _create_text(self):
        self.text_surface = self.font.render(self.text, True, Constants.white)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = self.rect.center
    
    # draw button and text on screen 
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    
    # check if button was clicked
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)