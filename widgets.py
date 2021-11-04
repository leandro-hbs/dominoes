import pygame as pg

class Button:
    def __init__(self, x, y, computer = ''):
        self.color = (255,255,255)
        self.computer = computer
        self.rect = pg.Rect(x, y, 250, 40)
        self.pos = (x+70, y+10)
    
    # Verifica se a posição do mouse toca a área do botão
    def verify(self, pos):
        if self.rect.collidepoint(pos):
            self.color = (0,128,0)
        else:
            self.color = (255,255,255)

class Images:
    def __init__(self):
        self.zero = pg.image.load('images\\zero.png')
        self.zero = pg.transform.scale(self.zero, (int(125*0.25), int(125*0.25)))
        self.one = pg.image.load('images\\one.png')
        self.one = pg.transform.scale(self.one, (int(125*0.25), int(125*0.25)))
        self.two = pg.image.load('images\\two.png')
        self.two = pg.transform.scale(self.two, (int(125*0.25), int(125*0.25)))
        self.three = pg.image.load('images\\three.png')
        self.three = pg.transform.scale(self.three, (int(125*0.25), int(125*0.25)))
        self.four = pg.image.load('images\\four.png')
        self.four = pg.transform.scale(self.four, (int(125*0.25), int(125*0.25)))
        self.five = pg.image.load('images\\five.png')
        self.five = pg.transform.scale(self.five, (int(125*0.25), int(125*0.25)))
        self.six = pg.image.load('images\\six.png')
        self.six = pg.transform.scale(self.six, (int(125*0.25), int(125*0.25)))

    # Retorna a imagem correspondente a peça recebida
    def load_piece(self, piece):
        image_piece = []
        
        if piece[0] == 0: 
            image_piece.append(self.zero)
        elif piece[0] == 1:
            image_piece.append(self.one)
        elif piece[0] == 2:
            image_piece.append(self.two)
        elif piece[0] == 3:
            image_piece.append(self.three)
        elif piece[0] == 4:
            image_piece.append(self.four)
        elif piece[0] == 5:
            image_piece.append(self.five)
        elif piece[0] == 6:
            image_piece.append(self.six)
        
        if piece[1] == 0:
            image_piece.append(self.zero)
        elif piece[1] == 1:
            image_piece.append(self.one)
        elif piece[1] == 2:
            image_piece.append(self.two)
        elif piece[1] == 3:
            image_piece.append(self.three)
        elif piece[1] == 4:
            image_piece.append(self.four)
        elif piece[1] == 5:
            image_piece.append(self.five)
        elif piece[1] == 6:
            image_piece.append(self.six)
        
        return image_piece

class Piece:
    def __init__(self, x, y, piece):
        self.color = (255,255,255)
        self.piece = piece
        self.rect = pg.Rect(x, y, 30, 60)
        self.selected = False

class Controller:
    def __init__(self, edge, x, y, direction) -> None:
        self.edge = edge
        self.x = x
        self.y = y
        self.direction = direction
        self.rect = pg.Rect(x, y, 30, 30)

    def update(self, piece):
        if piece[0] == self.edge:
            self.edge = piece[1]
        if piece[1] == self.edge:
            self.edge = piece[0]
    
    def ajust(self):
        if self.direction == 'right':
            if self.x + 60 < 640:
                self.x += 60
                self.rect = pg.Rect(self.x, self.y, 30, 30)
        if self.direction == 'left':
            if self.x - 60 > 0:
                self.x -= 60
                self.rect = pg.Rect(self.x, self.y, 30, 30)