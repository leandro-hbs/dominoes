import random
import json
import ast
from datetime import datetime
import pygame as pg
from pygame.constants import KEYDOWN, K_0, K_1, K_KP_ENTER, K_KP_PLUS, K_LEFT, K_RIGHT, QUIT

class Computer():
    def __init__(self):
        self.hand = []
        # Número inicial de peças na mão
        self.number = 3

    def distribute(self, pieces):
        self.hand = []
        for _ in range(self.number):
            self.hand.append(pieces[0])
            del pieces[0]
        return pieces
    
    def biggest_cart(self):
        has_cart = -1
        for piece in self.hand:
            if piece[0] == piece[1]:
                if piece[0] > has_cart:
                    has_cart = piece[0]
        return has_cart

    def remove_from_hand(self, piece):
        self.hand.remove(piece)

    def add_to_hand(self, piece):
        self.hand.append(piece)
                
    def can_play(self, left, right):
        for piece in self.hand:
            if piece[0] == left[0] or piece[1] == left[0] or piece[1] == right[0] or piece[1] == right[0]:
                return True
        return False
    
    def select_piece_to_play(self, left, right):
        for piece in self.hand:
            if piece[0] == left[0]:
                # Peça e borda
                return [piece, 'Left']
            if piece[1] == left[0]:
                return [piece, 'Left']
            if piece[0] == right[0]: 
                return [piece, 'Right']
            if piece[1] == right[0]:
                return [piece, 'Right']

class Human():
    def __init__(self):
        self.hand = []
        # Número inicial de peças na mão
        self.number = 3

    def distribute(self, pieces):
        self.hand = []
        for _ in range(self.number):
            self.hand.append(pieces[0])
            del pieces[0]
        return pieces
    
    def biggest_cart(self):
        has_cart = -1
        for piece in self.hand:
            if piece[0] == piece[1]:
                if piece[0] > has_cart:
                    has_cart = piece[0]
        return has_cart

    def remove_from_hand(self, piece):
        self.hand.remove(piece)

    def add_to_hand(self, piece):
        self.hand.append(piece)
                
    def can_play(self, left, right):
        for piece in self.hand:
            if piece[0] == left[0] or piece[1] == left[0] or piece[1] == right[0] or piece[1] == right[0]:
                return True
        return False

class Game:
    def __init__(self):
        pg.init()
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]
        self.player1 = Computer()
        self.player2 = Human()
        self.game = 1
        self.hand1 = 3
        self.hand2 = 3
        self.clock = pg.time.Clock()
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

    def create_screen(self):

        # Criando a tela
        self.heith = 700
        self.width = 1470
        self.screen = pg.display.set_mode((self.width, self.heith))
        pg.display.set_caption("Dominó")
        self.icon = pg.image.load('images\logo.png')
        pg.display.set_icon(self.icon)
        self.screen.fill((0,0,0))
        pg.display.update()

    def set_variables(self):

        # Ajustando as variaveis
        self.field = []
        for _ in range(10):
            line = []
            for _ in range(21):
                line.append(0)
            self.field.append(line)
        self.rest = []
        self.winner = 0
        self.selected = 0
        self.edge = 'Left'

        # Variáveis de controle
        self.round = 1
        self.running = True
        self.first_play = 0

        # Distribuindo as peças
        self.shuffle = random.sample(self.pieces, len(self.pieces))
        self.player1.number = self.hand1
        self.player2.number = self.hand2
        self.shuffle = self.player1.distribute(self.shuffle)
        self.shuffle = self.player2.distribute(self.shuffle)
        self.rest = self.shuffle
        
        # Número na borda, posição da próxima peça [y, x], -1              0           1           2
        #                                           esquerda        baixo       direita     cima
        self.left_controller = []
        self.right_controller = []
        
    
    def load_piece(self, piece):
        image_piece = []
        if piece[0] == 0: 
            image_piece.append(self.zero)
        if piece[1] == 0:
            image_piece.append(self.zero)
        if piece[0] == 1:
            image_piece.append(self.one)
        if piece[1] == 1:
            image_piece.append(self.one)
        if piece[0] == 2:
            image_piece.append(self.two)
        if piece[1] == 2:
            image_piece.append(self.two)
        if piece[0] == 3:
            image_piece.append(self.three)
        if piece[1] == 3:
            image_piece.append(self.three)
        if piece[0] == 4:
            image_piece.append(self.four)
        if piece[1] == 4:
            image_piece.append(self.four)
        if piece[0] == 5:
            image_piece.append(self.five)
        if piece[1] == 5:
            image_piece.append(self.five)
        if piece[0] == 6:
            image_piece.append(self.six)
        if piece[1] == 6:
            image_piece.append(self.six)
        return image_piece

    def put_piece_on_field(self, piece, position, rotate):     
        if piece[0] == piece[1]:
            self.field[position[0]][position[1]] = [piece, rotate+90]
        else:
            self.field[position[0]][position[1]] = [piece, rotate]
        self.clock.tick(5)

    def can_go_top(self, y, x):
        if y - 1 > 0:
            if self.field[y-1][x] == 0:
                return True
        return False 
    
    def can_go_bottom(self, y, x):
        if y + 1 < 10:
            if self.field[y+1][x] == 0:
                return True
        return False

    def can_go_left(self, y, x):
        if x - 1 > 0:
            if self.field[y][x-1] == 0:
                return True
        return False

    def can_go_right(self, y, x):
        if x + 1 < 21:
            if self.field[y][x+1] == 0:
                return True
        return False

    def adjust_right_position(self):
        y = self.right_controller[1][0]
        x = self.right_controller[1][1]

        if self.can_go_right(y,x):
            self.right_controller[1] = [y, x+1]
            self.right_controller[2] = 1
        elif self.can_go_left(y,x):
            self.right_controller[1] = [y, x-1]
            self.right_controller[2] = -1
        elif self.can_go_top(y,x):
            self.right_controller[1] = [y-1, x]
            self.right_controller[2] = 2
        elif self.can_go_bottom(y,x):
            self.right_controller[1] = [y+1, x]
            self.right_controller[2] = 0
    
    def adjust_left_position(self):
        y = self.left_controller[1][0]
        x = self.left_controller[1][1]

        if self.can_go_right(y,x):
            self.left_controller[1] = [y, x+1]
            self.left_controller[2] = 1
        elif self.can_go_left(y,x):
            self.left_controller[1] = [y, x-1]
            self.left_controller[2] = -1
        elif self.can_go_top(y,x):
            self.left_controller[1] = [y-1, x]
            self.left_controller[2] = 2
        elif self.can_go_bottom(y,x):
            self.left_controller[1] = [y+1, x]
            self.left_controller[2] = 0
        
    def load_field(self):

        # Percorre a matriz do campo
        for line in range(int(self.heith/70)):
            for column in range(int(self.width/70)):
                if self.field[line][column] != 0:

                    # Coleta as informações da peça
                    piece = self.load_piece(self.field[line][column][0])
                    rotate = self.field[line][column][1]

                    # Pega as coordenadas da peça
                    x = column*70
                    y = line*70

                    # Ajusta a rotação da peça
                    if rotate == 0:
                        self.screen.blit(piece[0], (x, y+15))
                        self.screen.blit(piece[1], (x+30, y+15))
                    if rotate == 90:
                        self.screen.blit(piece[0], (x+15, y+30))
                        self.screen.blit(piece[1], (x+15, y))
                    if rotate == 180:
                        self.screen.blit(piece[1], (x, y+15))
                        self.screen.blit(piece[0], (x+30, y+15))
                    if rotate == 270:
                        self.screen.blit(piece[1], (x+15, y))
                        self.screen.blit(piece[0], (x+15, y+30))
    
    def load_interface(self):

        # Setando posições e cores iniciais
        x1 = 575
        y1 = 300
        x2 = 50
        y2 = 300
        color_right = (255,255,255)
        color_left = (255,255,255)
        font = pg.font.Font(pg.font.get_default_font(), 20)

        for i in range(len(self.player2.hand)):

            # Marcando o item selecionado
            index = font.render(str(i), True, (255,255,255))
            if self.selected == i:
                index = font.render(str(i), True, (0,128,0))
            
            # Posicionado a peça
            piece = self.load_piece(self.player2.hand[i])
            self.screen.blit(piece[0], (y1, x1))
            self.screen.blit(piece[1], (y1, x1+30))
            self.screen.blit(index, (y1+9,x1+75))

            # Ajustando para nova peça
            y1 += 50

            # Mostrando a mão do oponente
        for i in range(len(self.player1.hand)):
            piece = self.load_piece([0,0])
            self.screen.blit(piece[0], (y2, x2))
            self.screen.blit(piece[1], (y2, x2+30))
            y2 += 50
        
        # Marcando a borda selecionada
        if self.edge == 'Left':
            color_left = (0,128,0)
        if self.edge == 'Right':
            color_right = (0,128,0)
        
        # Mostrando informações atuais
        text_comands = [ "Jogo: " + str(self.game),"Rodada: " + str(self.round) ,"Resto: " + str(len(self.rest)), "'0' = Left", "'1' = Right", "'< / >' = Alterna as peças"]
        position = 25
        for text in text_comands:
            text = font.render(text, True, (255,255,255))
            self.screen.blit(text, (1150,position))
            position+=25
        text_left = font.render('Left', True, color_left)
        self.screen.blit(self.left, (1150,600))
        self.screen.blit(text_left, (1160,675))
        text_right = font.render('Right', True, color_right)
        self.screen.blit(self.right, (1250,600))
        self.screen.blit(text_right, (1260,675))
        self.clock.tick(5)

    def start(self):

        # Iniciando com carroça
        cart1 = self.player1.biggest_cart()
        cart2 = self.player2.biggest_cart()
        y = int((self.heith/70)/2)
        x = int((self.width/70)/2)
        if cart1 > cart2:
            self.put_piece_on_field([cart1, cart1], [y, x], 0)
            self.player1.remove_from_hand([cart1, cart1])
            self.round += 1
            self.first_play = 1
            self.right_controller = [cart1, [y, x+1], 1]
            self.left_controller = [cart1, [y, x-1], -1]
        elif cart2 > cart1:
            self.put_piece_on_field([cart2, cart2], [y, x], 0)
            self.player2.remove_from_hand([cart2, cart2])
            self.round += 1
            self.first_play = 2
            self.right_controller = [cart2, [y, x+1], 1]
            self.left_controller = [cart2, [y, x-1], -1]
        else:
            self.put_piece_on_field(self.player1.hand[0], [y, x], 0)
            self.left_controller = [self.player1.hand[0][0], [y, x-1], -1]
            self.right_controller = [self.player1.hand[0][1], [y, x+1], 1]
            self.player1.remove_from_hand(self.player1.hand[0])
            self.round += 1
            self.first_play = 1

    def ComputerVsComputer(self):
        if (self.round + self.first_play) % 2 == 0:
            if self.player1.can_play(self.left_controller, self.right_controller):
                # Escolher peça na mão
                piece_edge = self.player1.select_piece_to_play(self.left_controller, self.right_controller)
                # Tirar peça da mão
                self.player1.remove_from_hand(piece_edge[0])
                # Adicionar o round
                self.round += 1
                # Decidir qual borda
                if piece_edge[1] == 'Right':
                    # Ajustar a peça para encaixar
                    if self.right_controller[0] == piece_edge[0][0]:
                        # Selecionar a rotação da peça
                        if self.right_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                            self.right_controller[0] = piece_edge[0][1]

                    elif self.right_controller[0] == piece_edge[0][1]:
                         # Selecionar a rotação da peça
                        if self.right_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                            self.right_controller[0] = piece_edge[0][0]
                    
                    # Ajustar a proxima posição e direção
                    self.adjust_right_position()
                    
                elif piece_edge[1] == 1:
                    # Ajustar a peça para encaixar
                    if self.left_controller[0] == piece_edge[0][0]:
                        # Selecionar a rotação da peça
                        if self.left_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                            self.left_controller[0] = piece_edge[0][1]

                    elif self.left_controller[0] == piece_edge[0][1]:
                         # Selecionar a rotação da peça
                        if self.left_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                            self.left_controller[0] = piece_edge[0][0]
                    
                    # Ajustar a proxima posição e direção
                    self.adjust_left_position()
            else:
                self.player1.add_to_hand(self.rest[0])
                del self.rest[0]
        if (self.round + self.first_play) % 2 == 1:
            if self.player2.can_play(self.left_controller, self.right_controller):
                piece_edge = self.player2.select_piece_to_play(self.left_controller, self.right_controller)
                self.player2.remove_from_hand(piece_edge[0])
                # Adicionar o round
                self.round += 1
                # Decidir qual borda
                if piece_edge[1] == 'Right':
                    # Ajustar a peça para encaixar
                    if self.right_controller[0] == piece_edge[0][0]:
                        # Selecionar a rotação da peça
                        if self.right_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                            self.right_controller[0] = piece_edge[0][1]
                        if self.right_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                            self.right_controller[0] = piece_edge[0][1]

                    elif self.right_controller[0] == piece_edge[0][1]:
                         # Selecionar a rotação da peça
                        if self.right_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                            self.right_controller[0] = piece_edge[0][0]
                        if self.right_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                            self.right_controller[0] = piece_edge[0][0]

                    # Ajustar a proxima posição e direção
                    self.adjust_right_position()
                    
                elif piece_edge[1] == 1:
                    # Ajustar a peça para encaixar
                    if self.left_controller[0] == piece_edge[0][0]:
                        # Selecionar a rotação da peça
                        if self.left_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                            self.left_controller[0] = piece_edge[0][1]
                        if self.left_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                            self.left_controller[0] = piece_edge[0][1]

                    elif self.left_controller[0] == piece_edge[0][1]:
                         # Selecionar a rotação da peça
                        if self.left_controller[2] == -1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 1:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 0:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                            self.left_controller[0] = piece_edge[0][0]
                        if self.left_controller[2] == 2:
                            self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                            self.left_controller[0] = piece_edge[0][0]
                    
                    # Ajustar a proxima posição e direção
                    self.adjust_left_position()
            else:
                self.player2.add_to_hand(self.rest[0])
                del self.rest[0]
    
    def Random(self):
        if self.player1.can_play(self.left_controller, self.right_controller):
            # Escolher peça na mão
            piece_edge = self.player1.select_piece_to_play(self.left_controller, self.right_controller)
            # Tirar peça da mão
            self.player1.remove_from_hand(piece_edge[0])
            # Adicionar o round
            self.round += 1
            # Decidir qual borda
            if piece_edge[1] == 'Right':
                # Ajustar a peça para encaixar
                if self.right_controller[0] == piece_edge[0][0]:
                    # Selecionar a rotação da peça
                    if self.right_controller[2] == -1:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                        self.right_controller[0] = piece_edge[0][1]
                    if self.right_controller[2] == 1:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                        self.right_controller[0] = piece_edge[0][1]
                    if self.right_controller[2] == 0:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                        self.right_controller[0] = piece_edge[0][1]
                    if self.right_controller[2] == 2:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                        self.right_controller[0] = piece_edge[0][1]

                elif self.right_controller[0] == piece_edge[0][1]:
                        # Selecionar a rotação da peça
                    if self.right_controller[2] == -1:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                        self.right_controller[0] = piece_edge[0][0]
                    if self.right_controller[2] == 1:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                        self.right_controller[0] = piece_edge[0][0]
                    if self.right_controller[2] == 0:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                        self.right_controller[0] = piece_edge[0][0]
                    if self.right_controller[2] == 2:
                        self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                        self.right_controller[0] = piece_edge[0][0]
                
                # Ajustar a proxima posição e direção
                self.adjust_right_position()
                
            elif piece_edge[1] == 'Left':
                # Ajustar a peça para encaixar
                if self.left_controller[0] == piece_edge[0][0]:
                    # Selecionar a rotação da peça
                    if self.left_controller[2] == -1:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                        self.left_controller[0] = piece_edge[0][1]
                    if self.left_controller[2] == 1:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                        self.left_controller[0] = piece_edge[0][1]
                    if self.left_controller[2] == 0:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                        self.left_controller[0] = piece_edge[0][1]
                    if self.left_controller[2] == 2:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                        self.left_controller[0] = piece_edge[0][1]

                elif self.left_controller[0] == piece_edge[0][1]:
                        # Selecionar a rotação da peça
                    if self.left_controller[2] == -1:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                        self.left_controller[0] = piece_edge[0][0]
                    if self.left_controller[2] == 1:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                        self.left_controller[0] = piece_edge[0][0]
                    if self.left_controller[2] == 0:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                        self.left_controller[0] = piece_edge[0][0]
                    if self.left_controller[2] == 2:
                        self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                        self.left_controller[0] = piece_edge[0][0]
                
                # Ajustar a proxima posição e direção
                self.adjust_left_position()
    
    def update(self):
        self.screen.fill((0,0,0))
        self.load_field()
        self.load_interface()
        pg.display.update()
    
    def data(self):
        return {
            'Turno': self.round,
            'Campo': self.field,
            'Player1': self.player1.hand,
            'Player2': self.player2.hand
        }        

    def play(self):
        self.create_screen()
        self.set_variables()
        self.start()
        self.update()
        self.info = ''
        while self.running:
            self.info += str(self.data()) + ','
            if len(self.player1.hand) == 0:
                self.winner = 1
                self.hand2 += 1
                self.game += 1
                self.running = False
            elif len(self.player2.hand) == 0:
                self.winner = 2
                self.game += 1
                self.hand1 += 1
                self.running = False
            elif self.winner == 0:
                if (self.round + self.first_play) % 2 == 0:
                    if self.player1.can_play(self.left_controller, self.right_controller):
                        self.Random()
                        self.update()
                    else:
                        if len(self.rest) > 0:
                            self.player1.add_to_hand(self.rest[0])
                            del self.rest[0]
                        else:
                            if self.player2.can_play(self.left_controller, self.right_controller):
                                # Adicionar o round
                                self.round += 1
                            else:
                                if len(self.player1.hand) > len(self.player2.hand):
                                    self.winner = 2
                                    self.game += 1
                                    self.hand1 += 1
                                    self.running = False
                                else:
                                    self.winner = 1
                                    self.hand2 += 1
                                    self.game += 1
                                    self.running = False

                if (self.round + self.first_play) % 2 == 1:
                    my_turn = True
                    if self.player2.can_play(self.left_controller, self.right_controller):
                        # Adicionar o round
                        self.round += 1
                        while my_turn:
                            for event in pg.event.get():
                                if event.type == QUIT:
                                    self.running = False
                                if event.type == KEYDOWN:
                                    if event.key == K_LEFT:
                                        if self.selected - 1 > - 1:
                                            self.selected -= 1
                                            self.update()
                                    elif event.key == K_RIGHT:
                                        if self.selected + 1 < len(self.player2.hand):
                                            self.selected += 1
                                            self.update()
                                    elif event.key == K_0:
                                        self.edge = 'Right'
                                        self.update()
                                    elif event.key == K_1:
                                        self.edge = 'Left'
                                        self.update()
                                    elif event.key == K_KP_ENTER:
                                        piece_edge = [self.player2.hand[self.selected], self.edge]
                                        if piece_edge[1] == 'Right':
                                            if piece_edge[0][0] == self.right_controller[0]:
                                                if self.selected - 1 > - 1:
                                                    self.selected -= 1
                                                self.player2.remove_from_hand(piece_edge[0])
                                                # Selecionar a rotação da peça
                                                if self.right_controller[2] == -1:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                                                    self.right_controller[0] = piece_edge[0][1]
                                                if self.right_controller[2] == 1:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                                                    self.right_controller[0] = piece_edge[0][1]
                                                if self.right_controller[2] == 0:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                                                    self.right_controller[0] = piece_edge[0][1]
                                                if self.right_controller[2] == 2:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                                                    self.right_controller[0] = piece_edge[0][1]
                                                self.update()
                                                # Ajustar a proxima posição e direção
                                                self.adjust_right_position()
                                                my_turn = False

                                            elif piece_edge[0][1] == self.right_controller[0]:
                                                if self.selected - 1 > - 1:
                                                    self.selected -= 1
                                                self.player2.remove_from_hand(piece_edge[0])
                                                # Selecionar a rotação da peça
                                                if self.right_controller[2] == -1:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 0)
                                                    self.right_controller[0] = piece_edge[0][0]
                                                if self.right_controller[2] == 1:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 180)
                                                    self.right_controller[0] = piece_edge[0][0]
                                                if self.right_controller[2] == 0:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 90)
                                                    self.right_controller[0] = piece_edge[0][0]
                                                if self.right_controller[2] == 2:
                                                    self.put_piece_on_field(piece_edge[0], self.right_controller[1], 270)
                                                    self.right_controller[0] = piece_edge[0][0]
                                                self.update()
                                                # Ajustar a proxima posição e direção
                                                self.adjust_right_position()
                                                my_turn = False

                                        if piece_edge[1] == 'Left':
                                            # Ajustar a peça para encaixar
                                            if self.left_controller[0] == piece_edge[0][0]:
                                                if self.selected - 1 > - 1:
                                                    self.selected -= 1
                                                self.player2.remove_from_hand(piece_edge[0])
                                                # Selecionar a rotação da peça
                                                if self.left_controller[2] == -1:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                                                    self.left_controller[0] = piece_edge[0][1]
                                                if self.left_controller[2] == 1:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                                                    self.left_controller[0] = piece_edge[0][1]
                                                if self.left_controller[2] == 0:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                                                    self.left_controller[0] = piece_edge[0][1]
                                                if self.left_controller[2] == 2:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                                                    self.left_controller[0] = piece_edge[0][1]
                                                self.update()
                                                # Ajustar a proxima posição e direção
                                                self.adjust_left_position()
                                                my_turn = False

                                            elif self.left_controller[0] == piece_edge[0][1]:
                                                if self.selected - 1 > - 1:
                                                    self.selected -= 1
                                                self.player2.remove_from_hand(piece_edge[0])
                                                # Selecionar a rotação da peça
                                                if self.left_controller[2] == -1:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 0)
                                                    self.left_controller[0] = piece_edge[0][0]
                                                if self.left_controller[2] == 1:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 180)
                                                    self.left_controller[0] = piece_edge[0][0]
                                                if self.left_controller[2] == 0:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 90)
                                                    self.left_controller[0] = piece_edge[0][0]
                                                if self.left_controller[2] == 2:
                                                    self.put_piece_on_field(piece_edge[0], self.left_controller[1], 270)
                                                    self.left_controller[0] = piece_edge[0][0]
                                                self.update()
                                                # Ajustar a proxima posição e direção
                                                self.adjust_left_position()
                                                my_turn = False
                    else:
                        if len(self.rest) > 0:
                            self.player2.add_to_hand(self.rest[0])
                            del self.rest[0]
                            self.update()
                        else:
                            # Adicionar o round
                            self.round += 1
                                             
game = Game()
data = []
while True:
    if game.hand1 == 14:
        break
    if game.hand2 == 14:
        break
    game.play()
    jogo = {
        'Jogo': game.game,
        'Resultado': game.winner,
        'Rodadas': ast.literal_eval(game.info[:-1])
    }
    data.append(jogo)
name = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
arquivo = open(name + '.json',"a")
jogo = json.dumps(data)
arquivo.write(jogo)
arquivo.close()
