class Domino:
    def __init__(self):
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]
        self.game = 1

    # Ajusta as variáveis
    def set_variables(self):  
        self.rest = self.pieces
        self.field = []

    # Retorna quem começa a rodada
    def who_start(self, pieces):
        cart = -1
        value = -1
        piece = []

        # Percorre as peças na mão e compara
        for p in pieces:
            if p[0] == p[1]:
                if p[0] > cart:
                    cart = p[0]
                    
        # Se não houver carroça, inicia a maior peça
        if cart == -1:
            for p in pieces:
                if p[0] + p[1] > value:
                    value = p[0] + p[1]
                    piece = p
            return piece
        else:
            return [cart, cart]