class Player():
    def __init__(self):
        self.name = "Human"
        self.hand = []
        self.number = 3

    # Distribui de peças
    def distribute(self, pieces):
        self.hand = []
        for _ in range(self.number):
            self.hand.append(pieces[0])
            del pieces[0]
        return pieces

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

    def select_piece_to_play(self, left, right):
        # Retorna a primeira peça que pode ser jogada e a borda a ser jogada
        for piece in self.hand:
            if piece[0] == left:
                return [piece, 'Left']
            if piece[1] == left:
                return [piece, 'Left']
            if piece[0] == right: 
                return [piece, 'Right']
            if piece[1] == right:
                return [piece, 'Right']