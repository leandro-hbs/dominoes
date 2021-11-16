from pygame import image
from domino import Domino
from player import Player
from computer import H1
from computer import H2
from computer import KNN
import pygame as pg
from widgets import Button, Controller, Images, Option, Piece

import random

class Game:
    def __init__(self):
        pg.init()
        self.domino = Domino()
        self.images = Images()
        self.player1 = Player()
        self.player2 = Player()
        self.clock = pg.time.Clock()
        self.page = 1
        self.result = "Venceu"
        self.rest = pg.Rect(560, 400, 60, 60)
        self.conf = pg.Rect(575, 30, 20, 20)
        self.show_resolutions = False
        self.resolutions = []
        
        # Salvando a font que será usada
        self.min_font = pg.font.Font(pg.font.get_default_font(), 10)
        self.font = pg.font.Font(pg.font.get_default_font(), 20)

        # Salvando as cores que serão utilizadas
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.green = (0,128,0)

        # Salvando a lista de botões
        self.buttons = []

        # Salvando peças clicavéis e peça marcada
        self.clickable_pieces = []
        self.marked_piece = []

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
    
    def load_interface(self):

        # Posição de referência
        y = 400
        x = 150

        # Desenhando o nome do jogador
        self.screen.blit(self.font.render(self.player1.name, True, self.white), (x-100, y+20))

        # Limpa a lista de peças clicavéis
        self.clickable_pieces = []
        
        # Carregando a mão do jogador
        for piece in self.player1.hand:
            image0 = self.images.load_piece(piece[0])
            image1 = self.images.load_piece(piece[1])
            # Desenha a peça
            self.screen.blit(image0, (x, y))
            self.screen.blit(image1, (x, y+30))

            # Adiciona peça na lista
            self.clickable_pieces.append(Piece(x,y,piece))

            # Ajustando posição
            x+=40

        # Posição de referência
        y = 20
        x = 150

        # Desenhando "Escolha o oponente"
        self.screen.blit(self.font.render(self.player2.name, True, self.white), (x-100, y+20))

        # Carregando a mão do oponente
        for _ in range(len(self.player2.hand)):
            image = self.images.load_piece(0)

            # Desenha a peça
            self.screen.blit(image, (x, y))
            self.screen.blit(image, (x, y+30))

            # Ajustando posição
            x+=40
        
        # Mostrando o resto
        image = self.images.load_piece(0)

        # Desenhando "Resto"
        self.screen.blit(self.font.render("Resto", True, self.white), (560, 375))

        # Desenha a peça
        self.screen.blit(image, (560, 400))
        self.screen.blit(image, (590, 400))
        self.screen.blit(image, (560, 430))
        self.screen.blit(image, (590, 430))

        # Mostrando botão de configuração
        if self.show_resolutions:
            self.screen.blit(self.font.render("-", True, self.white), (580, 30))
            pg.draw.rect(self.screen, self.white, self.conf, 2)
            for res in self.resolutions:
                pg.draw.rect(self.screen, res.color, res.rect, 2)
                self.screen.blit(self.min_font.render(str(res.height)+'x'+str(res.width), True, res.color), res.pos)
                res.verify(self.mouse)
                if res.rect.collidepoint(self.mouse):
                    if pg.mouse.get_pressed()[0] == 1:
                        self.screen = pg.display.set_mode((res.height, res.width))
                
        else: 
            self.screen.blit(self.font.render("+", True, self.white), (580, 30))
            pg.draw.rect(self.screen, self.white, self.conf, 2)


    def load_field(self):
        for piece_position in self.domino.field:
            # Coleta as informações da peça e sua posição
            image = self.images.load_piece(piece_position[0])
            position = piece_position[1]
            self.screen.blit(image, (position[0], position[1]))

    # Cria a primeira tela
    def first_screen(self):

        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.first_screen_y = 200
        self.first_screen_x = 150

        # Desenhando "Escolha o oponente"
        self.screen.blit(self.font.render("Escolha o oponente", True, self.white), (self.first_screen_y, self.first_screen_x-50))

        # Criando botões
        self.buttons.append(Button(self.first_screen_y, self.first_screen_x, H1()))
        self.buttons.append(Button(self.first_screen_y, self.first_screen_x+50, H2()))
        self.buttons.append(Button(self.first_screen_y, self.first_screen_x+100, KNN()))

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()

            # Desenhando os botões
            for button in self.buttons:
                pg.draw.rect(self.screen, button.color, button.rect, 2)
                self.screen.blit(self.font.render(button.computer.name, True, button.color), button.pos)
                button.verify(self.mouse)
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

        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.second_screen_x = 320
        self.second_screen_y = 255

        # Organizando o inicio do jogo
        self.domino.set_variables()
        self.domino.rest = self.player1.distribute(random.sample(self.domino.rest, len(self.domino.rest)))
        self.domino.rest = self.player2.distribute(random.sample(self.domino.rest, len(self.domino.rest)))

        # Verifica quem inicia
        piece = self.domino.who_start(self.player1.hand + self.player2.hand)

        # Se o jogador 1 começar
        if piece in self.player1.hand:
            self.player1.remove_from_hand(piece)

        # Se o jogador 2 começar
        else:
            self.player2.remove_from_hand(piece)
        
        if piece[0] == piece[1]:
            # Coloco a peça no meio da tela
            self.domino.field.append([piece[0], (self.second_screen_x, self.second_screen_y+15)])
            self.domino.field.append([piece[1], (self.second_screen_x, self.second_screen_y-15)])
            # Salvando os controladores // borda / posição central / top, left, bottom, right
            self.left_controller = Controller(piece[0], self.second_screen_x-30, self.second_screen_y, 'left')
            self.right_controller = Controller(piece[1], self.second_screen_x+30, self.second_screen_y, 'right')
        else:
            # Coloco a peça no meio da tela
            self.domino.field.append([piece[0], (self.second_screen_x, self.second_screen_y)])
            self.domino.field.append([piece[1], (self.second_screen_x-30, self.second_screen_y)])
            # Salvando os controladores // borda / posição central / top, left, bottom, right
            self.left_controller = Controller(piece[0], self.second_screen_x-30, self.second_screen_y, 'left')
            self.right_controller = Controller(piece[1], self.second_screen_x+60, self.second_screen_y, 'right')

        # Criando botões de resolução
        self.resolutions.append(Option(560, 70, 640, 480))
        self.resolutions.append(Option(560, 100, 800, 800))
        self.resolutions.append(Option(560, 130, 1280, 800))

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Preenchendo background
            self.screen.fill(self.black)

            # Desenhando o campo
            self.load_field()
            self.load_interface()

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()
            print(self.domino.field)
            if len(self.marked_piece) != 0:
                image0 = self.images.load_piece(self.marked_piece[0])
                image1 = self.images.load_piece(self.marked_piece[1])
                # Desenha a peça
                self.screen.blit(image0, (self.mouse[0]-15, self.mouse[1]-30))
                self.screen.blit(image1, (self.mouse[0]-15, self.mouse[1]))

            else:
                # Verificando a posição do mouse
                for piece in self.clickable_pieces:                
                    if piece.rect.collidepoint(self.mouse):
                        pg.draw.rect(self.screen, (0,128,0), piece.rect, 2)
                        if pg.mouse.get_pressed()[0] == 1:
                            self.marked_piece = piece.piece
                            self.player1.remove_from_hand(piece.piece)
                
                # Verifica se vai pegar do resto
                if self.rest.collidepoint(self.mouse):
                    pg.draw.rect(self.screen, (0,128,0), self.rest, 2)
                    if pg.mouse.get_pressed()[0] == 1:
                        self.player1.add_to_hand(self.domino.rest.pop())

                # Verifica se vai mudar resolução
                if self.conf.collidepoint(self.mouse):
                    pg.draw.rect(self.screen, (0,128,0), self.conf, 2)
                    if pg.mouse.get_pressed()[0] == 1:
                        self.show_resolutions = not self.show_resolutions

            # Verificando onde a peça vai ser colocada
            for event in pg.event.get():
                if pg.mouse.get_pressed()[0] == 1:
                    # Verifica se a peça foi colocada na direita
                    if self.right_controller.rect.collidepoint(self.mouse):
                        # Por a peça no campo
                        if self.marked_piece[0] == self.right_controller.edge:
                            self.right_controller.edge = self.marked_piece[1]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append([self.marked_piece[0], (self.right_controller.x, self.right_controller.y+15)])
                                self.domino.field.append([self.marked_piece[1], (self.right_controller.x, self.right_controller.y-15)])
                            else:
                                self.domino.field.append([self.marked_piece[0], (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append([self.marked_piece[1], (self.right_controller.x+30, self.right_controller.y)])
                        else:
                            self.right_controller.edge = self.marked_piece[0]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append([self.marked_piece[1], (self.right_controller.x, self.right_controller.y+15)])
                                self.domino.field.append([self.marked_piece[0], (self.right_controller.x, self.right_controller.y-15)])
                            else:
                                self.domino.field.append([self.marked_piece[1], (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append([self.marked_piece[0], (self.right_controller.x+30, self.right_controller.y)])
                            
                        # Ajusta a nova posição
                        if self.marked_piece[0] == self.marked_piece[1]:
                            self.right_controller.ajust(True)
                        else:
                            self.right_controller.ajust(False)
                        # Retirar peça da mão
                        self.marked_piece = []

                    # Verifica se a peça foi colocada na esquerda
                    if self.left_controller.rect.collidepoint(self.mouse):
                        # Por a peça no campo
                        if self.marked_piece[0] == self.left_controller.edge:
                            self.left_controller.edge = self.marked_piece[1]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append([self.marked_piece[0], (self.left_controller.x, self.left_controller.y+15)])
                                self.domino.field.append([self.marked_piece[1], (self.left_controller.x, self.left_controller.y-15)])
                            else:
                                self.domino.field.append([self.marked_piece[0], (self.left_controller.x, self.left_controller.y)])
                                self.domino.field.append([self.marked_piece[1], (self.left_controller.x-30, self.left_controller.y)])
                        else:
                            self.left_controller.edge = self.marked_piece[0]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append([self.marked_piece[1], (self.left_controller.x, self.left_controller.y+15)])
                                self.domino.field.append([self.marked_piece[0], (self.left_controller.x, self.left_controller.y-15)])
                            else:
                                self.domino.field.append([self.marked_piece[1], (self.left_controller.x, self.left_controller.y)])
                                self.domino.field.append([self.marked_piece[0], (self.left_controller.x-30, self.left_controller.y)])
                        # Ajusta a nova posição
                        if self.marked_piece[0] == self.marked_piece[1]:
                            self.left_controller.ajust(True)
                        else:
                            self.left_controller.ajust(False)
                        # Retirar peça da mão
                        self.marked_piece = []
                
                if event.type==pg.QUIT:
                    pg.quit()
                    exit(0)

            # Atualizando a tela
            pg.display.update()

    # Cria a terceira tela
    def third_screen(self):
        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.third_screen_y = 200
        self.third_screen_x = 200

        # Desenhando "Escolha o oponente"
        self.screen.blit(self.font.render("Você " + self.result, True, self.white), (self.third_screen_y+60, self.third_screen_x-50))

        # Criando botões
        button = Button(self.third_screen_y, self.third_screen_x)

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Desenhando o botão
            pg.draw.rect(self.screen, button.color, button.rect, 2)
            self.screen.blit(self.font.render('Novo Jogo', True, button.color), button.pos)

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()

            # Verificando a posição do mouse
            button.verify(self.mouse)

            if button.rect.collidepoint(self.mouse):
                if pg.mouse.get_pressed()[0] == 1:
                    self.page = 1
                    return
  
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    exit(0)
            
            # Atualizando a tela
            pg.display.update()