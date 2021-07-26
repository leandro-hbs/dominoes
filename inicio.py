import random
import pygame as pg
from pygame.constants import QUIT
import time

class Computer():
    def __init__(self):
        self.hand = []
        # Número inicial de peças na mão
        self.number = 3

    def distribute(self, pieces):
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
                return [piece, 1]
            if piece[1] == left[0]:
                return [piece, 1]
            if piece[0] == right[0]: 
                return [piece, 0]
            if piece[1] == right[0]:
                return [piece, 0]

class Human():
    def __init__(self):
        self.hand = []
        # Número inicial de peças na mão
        self.number = 3

    def distribute(self, pieces):
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

    def can_play(self, edges):
        for piece in self.hand:
            if piece[0] == edges[0] or piece[0] == edges[0] or piece[1] == edges[0] or piece[1] == edges[0]:
                return True
        return False

class Game:
    def __init__(self):
        pg.init()
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]

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
        self.edges = []
        self.rest = []
        self.winner = 0
        self.clock = pg.time.Clock()
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
        for line in range(int(self.heith/70)):
            for column in range(int(self.width/70)):
                if self.field[line][column] != 0:
                    piece = self.load_piece(self.field[line][column][0])
                    rotate = self.field[line][column][1]
                    x = column*70
                    y = line*70
                    if rotate == 0:
                        self.screen.blit(piece[0], (x, y+15))
                        self.screen.blit(piece[1], (x+30, y+15))
                    if rotate == 90:
                        self.screen.blit(piece[0], (x+15, y))
                        self.screen.blit(piece[1], (x+15, y+30))
                    if rotate == 180:
                        self.screen.blit(piece[1], (x, y+15))
                        self.screen.blit(piece[0], (x+30, y+15))
                    if rotate == 270:
                        self.screen.blit(piece[1], (x+15, y))
                        self.screen.blit(piece[0], (x+15, y+30))

    def start(self):

        # Variáveis de controle
        self.round = 1
        self.running = True
        self.first_play = 0

        # Distribuindo as peças
        self.shuffle = random.sample(self.pieces, len(self.pieces))
        self.player1 = Computer()
        self.shuffle = self.player1.distribute(self.shuffle)
        self.player2 = Computer()
        self.shuffle = self.player2.distribute(self.shuffle)
        self.rest = self.shuffle
        
        # Número na borda, posição da próxima peça [y, x], -1              0           1           2
        #                                           esquerda        baixo       direita     cima
        self.left_controller = []
        self.right_controller = []

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
            self.right_controller = [self.player1.hand[0][0], [y, x+1], 1]
            self.left_controller = [self.player1.hand[0][1], [y, x-1], -1]
            self.player1.remove_from_hand(self.player1.hand[0])
            self.round += 1
            self.first_play = 1

    def keep_play(self):
        if (self.round + self.first_play) % 2 == 0:
            if self.player1.can_play(self.left_controller, self.right_controller):
                # Escolher peça na mão
                piece_edge = self.player1.select_piece_to_play(self.left_controller, self.right_controller)
                # Tirar peça da mão
                self.player1.remove_from_hand(piece_edge[0])
                # Adicionar o round
                self.round += 1
                # Decidir qual borda
                if piece_edge[1] == 0:
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
                if piece_edge[1] == 0:
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
        if len(self.player1.hand) == 0:
                self.winner = 1
                print("Jogador 1 venceu")
        if len(self.player2.hand) == 0:
            self.winner = 2
            print("Jogador 2 venceu")
        if len(self.rest) == 0:
            if (self.round + self.first_play) % 2 == 0:
                self.winner = 2
                print("Jogador 2 venceu")
            if (self.round + self.first_play) % 2 == 1:
                self.winner = 1
                print("Jogador 1 venceu")
    
    def play(self):
        while self.running:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.running = False
            if self.winner == 0:  
                self.keep_play()
            self.load_field()
            pg.display.update()
        
game = Game()
game.create_screen()
game.set_variables()
game.start()
game.play()

