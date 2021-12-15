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
        self.conf = pg.Rect(575, 30, 20, 20)
        self.show_resolutions = False
        self.resolutions = []

        # Salvando a font que será usada
        self.min_font = pg.font.Font(pg.font.get_default_font(), 10)
        self.font = pg.font.Font(pg.font.get_default_font(), 20)

        # Salvando as cores que serão utilizadas
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 128, 0)

        # Salvando a lista de botões
        self.buttons = []

        # Salvando peças clicavéis e peça marcada
        self.clickable_pieces = []
        self.marked_piece = []

        # Tamanho da tela
        self.height = 480
        self.offset = [[0, 0], [100, 100], [300, 100]]
        self.index = 0
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
        y = self.height
        x = self.width

        # Desenhando o nome do jogador
        self.screen.blit(self.font.render(
            self.player1.name, True, self.white), (x/25, y-(y/10)))

        x = x/25+80
        y = y-(y/10)-20

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
            self.clickable_pieces.append(Piece(x, y, piece))

            # Ajustando posição
            x += 40

        # Posição de referência
        y = self.height
        x = self.width

        # Desenhando o nome do oponente
        self.screen.blit(self.font.render(
            self.player2.name, True, self.white), (x/25, (y/15)))

        x = x/25+80
        y = (y/15)-20

        # Carregando a mão do oponente
        for _ in range(len(self.player2.hand)):
            image = self.images.load_piece(0)

            # Desenha a peça
            self.screen.blit(image, (x, y))
            self.screen.blit(image, (x, y+30))

            # Ajustando posição
            x += 40

        # Mostrando o resto
        image = self.images.load_piece(0)

        # Posição de referência
        y = self.height
        x = self.width

        # Desenhando "Resto"
        self.screen.blit(self.font.render(
            str(len(self.domino.rest)), True, self.white), ((x*0.9)+5, (y*0.9)+5))
        self.rest = pg.Rect((x*0.9), (y*0.9), 35, 30)
        pg.draw.rect(self.screen, self.white, self.rest, 2)

        # Posição de referência
        y = self.height*0.05
        x = self.width*0.9

        # Criando botões de resolução
        self.resolutions = []
        self.resolutions.append(Option(x-10, y+40, 480, 640))
        self.resolutions.append(Option(x-10, y+70, 800, 800))
        self.resolutions.append(Option(x-10, y+100, 800, 1280))

        self.conf = pg.Rect(x, y, 30, 30)

        # Mostrando botão de configuração
        if self.show_resolutions:
            self.screen.blit(self.font.render(
                "-", True, self.white), (x+10, y+10))
            pg.draw.rect(self.screen, self.white, self.conf, 2)
            for res in self.resolutions:
                pg.draw.rect(self.screen, res.color, res.rect, 2)
                self.screen.blit(self.min_font.render(
                    str(res.width)+'x'+str(res.height), True, res.color), res.pos)
                res.verify(self.mouse)
                if res.rect.collidepoint(self.mouse):
                    if pg.mouse.get_pressed()[0] == 1:
                        self.index = self.resolutions.index(res)
                        self.left_controller.update_rect(
                            self.offset[self.index])
                        self.right_controller.update_rect(
                            self.offset[self.index])
                        self.height = res.height
                        self.width = res.width

        else:
            self.screen.blit(self.font.render(
                "*", True, self.white), (x+10, y+10))
            pg.draw.rect(self.screen, self.white, self.conf, 2)

    def load_field(self):
        for piece_position in self.domino.field:
            # Coleta as informações da peça e sua posição
            image = self.images.load_piece(piece_position[0])
            position = piece_position[1]
            self.screen.blit(
                image, (position[0]+self.offset[self.index][0], position[1]+self.offset[self.index][1]))

    # Cria a primeira tela
    def first_screen(self):

        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.first_screen_y = 200
        self.first_screen_x = 150

        # Desenhando "Escolha o oponente"
        self.screen.blit(self.font.render("Escolha o oponente", True,
                         self.white), (self.first_screen_y, self.first_screen_x-50))

        # Criando botões
        self.buttons.append(
            Button(self.first_screen_y, self.first_screen_x, H1()))
        self.buttons.append(
            Button(self.first_screen_y, self.first_screen_x+50, H2()))
        self.buttons.append(
            Button(self.first_screen_y, self.first_screen_x+100, KNN()))

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()

            # Desenhando os botões
            for button in self.buttons:
                pg.draw.rect(self.screen, button.color, button.rect, 2)
                self.screen.blit(self.font.render(
                    button.computer.name, True, button.color), button.pos)
                button.verify(self.mouse)
                if button.rect.collidepoint(self.mouse):
                    if pg.mouse.get_pressed()[0] == 1:
                        #self.player2 = button.computer
                        self.page = 2
                        return

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            # Atualizando a tela
            pg.display.update()

    # Cria a segunda tela
    def second_screen(self):

        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.second_screen_x = self.width/2
        self.second_screen_y = self.height/2

        # Organizando o inicio do jogo
        self.domino.set_variables()
        self.domino.rest = self.player1.distribute(
            random.sample(self.domino.rest, len(self.domino.rest)))
        self.domino.rest = self.player2.distribute(
            random.sample(self.domino.rest, len(self.domino.rest)))

        # Verifica quem inicia
        piece = self.domino.who_start(self.player1.hand + self.player2.hand)

        # Se o jogador 1 começar
        if piece in self.player1.hand:
            self.player1.remove_from_hand(piece)
            self.my_turn = 2

        # Se o jogador 2 começar
        else:
            self.player2.remove_from_hand(piece)
            self.my_turn = 1

        if piece[0] == piece[1]:
            # Coloco a peça no meio da tela
            self.domino.field.append(
                [piece[0], (self.second_screen_x, self.second_screen_y+15)])
            self.domino.field.append(
                [piece[1], (self.second_screen_x, self.second_screen_y-15)])
            # Salvando os controladores // borda / posição central / top, left, bottom, right
            self.left_controller = Controller(
                piece[0], self.second_screen_x-30, self.second_screen_y, 'left')
            self.right_controller = Controller(
                piece[1], self.second_screen_x+30, self.second_screen_y, 'right')
        else:
            # Coloco a peça no meio da tela
            self.domino.field.append(
                [piece[0], (self.second_screen_x, self.second_screen_y)])
            self.domino.field.append(
                [piece[1], (self.second_screen_x-30, self.second_screen_y)])
            # Salvando os controladores // borda / posição central / top, left, bottom, right
            self.left_controller = Controller(
                piece[1], self.second_screen_x-60, self.second_screen_y, 'left')
            self.right_controller = Controller(
                piece[0], self.second_screen_x+30, self.second_screen_y, 'right')

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Ajustando resolução da tela
            self.screen = pg.display.set_mode((self.width, self.height))

            # Preenchendo background
            self.screen.fill(self.black)

            # Desenhando o campo
            self.load_field()
            self.load_interface()

            # Se for turno do player
            if self.my_turn == 1:
                # Armazenando a posição do mouse
                self.mouse = pg.mouse.get_pos()
                if len(self.marked_piece) != 0:
                    image0 = self.images.load_piece(self.marked_piece[0])
                    image1 = self.images.load_piece(self.marked_piece[1])
                    # Desenha a peça
                    self.screen.blit(
                        image0, (self.mouse[0]-15, self.mouse[1]-30))
                    self.screen.blit(image1, (self.mouse[0]-15, self.mouse[1]))
                    if pg.mouse.get_pressed()[2] == 1:
                        self.player1.add_to_hand(self.marked_piece)
                        self.marked_piece = []

                else:
                    # Verificando a posição do mouse
                    for piece in self.clickable_pieces:
                        if piece.rect.collidepoint(self.mouse):
                            pg.draw.rect(
                                self.screen, (0, 128, 0), piece.rect, 2)
                            if pg.mouse.get_pressed()[0] == 1:
                                if self.player1.can_play_this_piece(piece.piece, self.left_controller.edge, self.right_controller.edge):
                                    self.marked_piece = piece.piece
                                    self.player1.remove_from_hand(piece.piece)

                    # Verifica se vai pegar do resto
                    if self.player1.can_play(self.left_controller.edge, self.right_controller.edge):
                        pass
                    else:
                        if self.rest.collidepoint(self.mouse):
                            pg.draw.rect(
                                self.screen, (0, 128, 0), self.rest, 2)
                            if pg.mouse.get_pressed()[0] == 1:
                                self.player1.add_to_hand(
                                    self.domino.rest.pop())

                    # Verifica se vai mudar resolução
                    if self.conf.collidepoint(self.mouse):
                        pg.draw.rect(self.screen, (0, 128, 0), self.conf, 2)
                        if pg.mouse.get_pressed()[0] == 1:
                            self.show_resolutions = not self.show_resolutions

                # Verificando onde a peça vai ser colocada
                if pg.mouse.get_pressed()[0] == 1:
                    # Verifica se a peça foi colocada na direita
                    if self.right_controller.rect.collidepoint(self.mouse):
                        # Pegar peça de encaixe e nova borda
                        if self.marked_piece[0] == self.right_controller.edge:
                            connect_piece = self.marked_piece[0]
                            border_piece = self.marked_piece[1]
                            self.right_controller.edge = self.marked_piece[1]
                        else:
                            connect_piece = self.marked_piece[1]
                            border_piece = self.marked_piece[0]
                            self.right_controller.edge = self.marked_piece[0]

                        # Por a peça no campo verificando se é carroça
                        if self.marked_piece[0] == self.marked_piece[1]:
                            # Verifica a direção
                            if self.right_controller.direction == 'right':
                                self.domino.field.append(
                                    [connect_piece, (self.right_controller.x, self.right_controller.y+15)])
                                self.domino.field.append(
                                    [border_piece, (self.right_controller.x, self.right_controller.y-15)])
                            if self.right_controller.direction == 'down':
                                self.domino.field.append(
                                    [connect_piece, (self.right_controller.x+15, self.right_controller.y)])
                                self.domino.field.append(
                                    [border_piece, (self.right_controller.x-15, self.right_controller.y)])
                        else:
                            # Verifica a direção
                            if self.right_controller.direction == 'right':
                                self.domino.field.append(
                                    [connect_piece, (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append(
                                    [border_piece, (self.right_controller.x+30, self.right_controller.y)])
                            if self.right_controller.direction == 'down':
                                self.domino.field.append(
                                    [connect_piece, (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append(
                                    [border_piece, (self.right_controller.x, self.right_controller.y+30)])

                        # Ajusta a nova posição
                        if self.marked_piece[0] == self.marked_piece[1]:
                            self.right_controller.ajust(
                                True)
                            self.right_controller.update_rect(
                                self.offset[self.index])
                        else:
                            self.right_controller.ajust(
                                False)
                            self.right_controller.update_rect(
                                self.offset[self.index])
                        # Retirar peça da mão
                        self.marked_piece = []
                        self.my_turn = 2

                    # Verifica se a peça foi colocada na esquerda
                    elif self.left_controller.rect.collidepoint(self.mouse):
                        print(self.left_controller.direction)
                        # Pegar peça de encaixe e nova borda
                        if self.marked_piece[0] == self.left_controller.edge:
                            connect_piece = self.marked_piece[0]
                            border_piece = self.marked_piece[1]
                            self.left_controller.edge = self.marked_piece[1]
                        else:
                            connect_piece = self.marked_piece[1]
                            border_piece = self.marked_piece[0]
                            self.left_controller.edge = self.marked_piece[0]

                        # Por a peça no campo verificando se é carroça
                        if self.marked_piece[0] == self.marked_piece[1]:
                            # Verifica a direção
                            if self.left_controller.direction == 'left':
                                self.domino.field.append(
                                    [connect_piece, (self.left_controller.x, self.left_controller.y+15)])
                                self.domino.field.append(
                                    [border_piece, (self.left_controller.x, self.left_controller.y-15)])
                            if self.left_controller.direction == 'up':
                                self.domino.field.append(
                                    [connect_piece, (self.left_controller.x+15, self.left_controller.y)])
                                self.domino.field.append(
                                    [border_piece, (self.left_controller.x-15, self.left_controller.y)])
                        else:
                            if self.left_controller.direction == 'left':
                                self.domino.field.append(
                                    [connect_piece, (self.left_controller.x, self.left_controller.y)])
                                self.domino.field.append(
                                    [border_piece, (self.left_controller.x-30, self.left_controller.y)])
                            if self.left_controller.direction == 'up':
                                self.domino.field.append(
                                    [connect_piece, (self.left_controller.x, self.left_controller.y+30)])
                                self.domino.field.append(
                                    [border_piece, (self.left_controller.x, self.left_controller.y)])

                        # Ajusta a nova posição
                        if self.marked_piece[0] == self.marked_piece[1]:
                            self.left_controller.ajust(
                                True)
                            self.left_controller.update_rect(
                                self.offset[self.index])
                        else:
                            self.left_controller.ajust(
                                False)
                            self.left_controller.update_rect(
                                self.offset[self.index])
                        # Retirar peça da mão
                        self.marked_piece = []
                        self.my_turn = 2

            # Se for turno da máquina
            elif self.my_turn == 2:
                # Se a máquina puder jogar
                if self.player2.can_play(self.left_controller.edge, self.right_controller.edge):
                    (self.marked_piece, position) = self.player2.select_piece_to_play(
                        self.left_controller.edge, self.right_controller.edge)
                    self.player2.remove_from_hand(self.marked_piece)
                    if position == 'Right':
                        if self.marked_piece[0] == self.right_controller.edge:
                            self.right_controller.edge = self.marked_piece[1]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.right_controller.x, self.right_controller.y+15)])
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.right_controller.x, self.right_controller.y-15)])
                            else:
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.right_controller.x+30, self.right_controller.y)])
                        else:
                            self.right_controller.edge = self.marked_piece[0]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.right_controller.x, self.right_controller.y+15)])
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.right_controller.x, self.right_controller.y-15)])
                            else:
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.right_controller.x, self.right_controller.y)])
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.right_controller.x+30, self.right_controller.y)])

                            # Ajusta a nova posição
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.right_controller.ajust(
                                    True)
                                self.right_controller.update_rect(
                                    self.offset[self.index])
                            else:
                                self.right_controller.ajust(
                                    False)
                                self.right_controller.update_rect(
                                    self.offset[self.index])
                            # Retirar peça da mão
                            self.marked_piece = []
                            self.my_turn = 1 

                    elif position == 'Left':
                        # Por a peça no campo
                        if self.marked_piece[0] == self.left_controller.edge:
                            self.left_controller.edge = self.marked_piece[1]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.left_controller.x, self.left_controller.y+15)])
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.left_controller.x, self.left_controller.y-15)])
                            else:
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.left_controller.x, self.left_controller.y)])
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.left_controller.x-30, self.left_controller.y)])
                        else:
                            self.left_controller.edge = self.marked_piece[0]
                            if self.marked_piece[0] == self.marked_piece[1]:
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.left_controller.x, self.left_controller.y+15)])
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.left_controller.x, self.left_controller.y-15)])
                            else:
                                self.domino.field.append(
                                    [self.marked_piece[1], (self.left_controller.x, self.left_controller.y)])
                                self.domino.field.append(
                                    [self.marked_piece[0], (self.left_controller.x-30, self.left_controller.y)])
                        # Ajusta a nova posição
                        if self.marked_piece[0] == self.marked_piece[1]:
                            self.left_controller.ajust(
                                True)
                            self.left_controller.update_rect(
                                self.offset[self.index])
                        else:
                            self.left_controller.ajust(
                                False)
                            self.left_controller.update_rect(
                                self.offset[self.index])
                        # Retirar peça da mão
                        self.marked_piece = []
                        self.my_turn = 1

                # Se não, adiciona uma peça do resto
                else:
                    self.player2.add_to_hand(self.domino.rest.pop())

            # Verifica vencedor
            if len(self.player1.hand) == 0:
                self.result = "Venceu"
                self.page = 3
                return
            if len(self.player2.hand) == 0:
                self.result = "Perdeu"
                self.page = 3
                return

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            # Atualizando a tela
            pg.display.update()

    # Cria a terceira tela
    def third_screen(self):
        # Preenchendo background
        self.screen.fill(self.black)

        # Posição de referência
        self.third_screen_y = self.height/2
        self.third_screen_x = self.width/2

        # Desenhando se venceu ou perdeu
        self.screen.blit(self.font.render("Você " + self.result, True,
                         self.white), (self.third_screen_x-75, self.third_screen_y-150))

        # Criando botões
        button = Button(self.third_screen_x-130, self.third_screen_y)

        while True:

            # 30 FPS
            self.clock.tick(30)

            # Desenhando o botão
            pg.draw.rect(self.screen, button.color, button.rect, 2)
            self.screen.blit(self.font.render(
                'Novo Jogo', True, button.color), button.pos)

            # Armazenando a posição do mouse
            self.mouse = pg.mouse.get_pos()

            # Verificando a posição do mouse
            button.verify(self.mouse)

            if button.rect.collidepoint(self.mouse):
                if pg.mouse.get_pressed()[0] == 1:
                    self.page = 1
                    return

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit(0)

            # Atualizando a tela
            pg.display.update()

    def reset(self):
        self.domino = Domino()
        self.player1 = Player()
        self.player2 = Player()
        self.page = 1
        self.result = "Venceu"
        self.show_resolutions = False
        self.marked_piece = []
