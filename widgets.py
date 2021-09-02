import pygame as pg

class Button:
    def __init__(self, x, y, computer):
        self.color = (255,255,255)
        self.computer = computer
        self.rect = pg.Rect(x, y, 250, 40)
        self.pos = (x+70, y+10)
    
    def verify(self, pos):
        if self.rect.collidepoint(pos):
            self.color = (0,128,0)
        else:
            self.color = (255,255,255)
