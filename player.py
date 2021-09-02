class Player():
    def __init__(self):
        # Nome
        self.name = "Human"
        # Peças na mão
        self.hand = []
        # Número inicial de peças na mão
        self.number = 3

    # Distribuição de peças
    def distribute(self, pieces):
        self.hand = []
        for _ in range(self.number):
            self.hand.append(pieces[0])
            del pieces[0]
        return pieces
    
    # Retorna a maior carroça na mão se houver
    def biggest_cart(self):
        cart = -1

        # Percorre as peças na mão e compara
        for piece in self.hand:
            if piece[0] == piece[1]:
                if piece[0] > cart:
                    cart = piece[0]
        return cart

    # Remove uma peça da mão
    def remove_from_hand(self, piece):
        self.hand.remove(piece)

    # Adiciona uma peça na mão
    def add_to_hand(self, piece):
        self.hand.append(piece)

    # Verifica se pode jogar
    def can_play(self, left, right):
        for piece in self.hand:
            if piece[0] == left[0] or piece[1] == left[0] or piece[0] == right[0] or piece[1] == right[0]:
                return True
        return False

    # Retorna o somatório dos valores das peças na mão
    def big_hand(self):
        value = 0
        for piece in self.hand:
            value += piece[0] + piece[1]
        return value
    
    # Retorna a maior peça na mão
    def big_piece(self):
        value = -1
        piece = []

        # Percorre as peças na mão e compara
        for p in self.hand:
            if p[0] + p[1] > value:
                value = p[0] + p[1]
                piece = p
        return piece