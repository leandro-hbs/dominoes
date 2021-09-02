from domino import Domino
from player import Player
from computer import H1
from computer import H2
from computer import KNN
import pygame as pg
from widgets import Button

class Game:
    def __init__(self):
        pg.init()

        # Jogo de dominó
        self.domino = Domino()

        # Player 1 = Human
        self.player1 = Player()

        # Controlador de páginas
        self.page = 1

        # Controlador de clock
        self.clock = pg.time.Clock()

        # Salvando a font que será usada
        self.font = pg.font.Font(pg.font.get_default_font(), 20)

        # Salvando as cores que serão utilizadas
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,128,0)

        # Salvando a lista de botões
        self.buttons = []

        # Salvando as imagens que serão utilizadas
        self.right = pg.image.load('images\\right.png')
        self.right = pg.transform.scale(self.right, (int(155*0.35), int(155*0.35)))
        self.left = self.right.copy()
        self.left = pg.transform.rotate(self.right, 180)
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

        # Tamanho da tela
        self.height = 480
        self.width = 640

        # Criando a tela e Adicionando título e icone
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Dominó")
        pg.display.set_icon(pg.image.load('images\logo.png'))

        # Preenchendo background
        self.screen.fill(self.black)
        pg.display.update()

    # Cria a primeira tela
    def first_screen(self):

        self.first_screen_x = 230
        self.first_screen_y = 50

        # Desenhando "Escolha o oponente"
        self.screen.blit(self.font.render("Escolha o oponente", True, self.white), (self.first_screen_x, self.first_screen_y))

        # Criando botões
        self.buttons.append(Button(self.first_screen_x-30, self.first_screen_y+100, H1()))
        self.buttons.append(Button(self.first_screen_x-30, self.first_screen_y+150, H2()))
        self.buttons.append(Button(self.first_screen_x-30, self.first_screen_y+200, KNN()))

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Desenhando os botões
            for button in self.buttons:
                pg.draw.rect(self.screen, button.color, button.rect, 2)
                self.screen.blit(self.font.render(button.computer.name, True, button.color), button.pos)

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()

            # Verificando a posição do mouse
            for button in self.buttons:
                button.verify(self.mouse)

            for button in self.buttons:
                if button.rect.collidepoint(self.mouse):
                    if pg.mouse.get_pressed()[0] == 1:
                        self.player2 = button.computer
                        self.page = 2
                        return
  
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    exit(0)
            
            # Atualizando a tela
            pg.display.update()
    
    # Cria a segunda tela
    def second_screen(self):
        # TO DO
        pass