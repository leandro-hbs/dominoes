class Domino:
    def __init__(self):
        self.pieces = [[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [1,2], [1,3], [1,4], [1,5], [1,6], [2,3], [2,4], [2,5], [2,6], [3,4], [3,5], [3,6], [4,5], [4,6], [5,6]]
        self.game = 1

    def set_variables(self):

        # Criando a matriz que representa o campo
        self.field = []
        for _ in range(10):
            line = []
            for _ in range(21):
                line.append(0)
            self.field.append(line)
        
        # Vetor que armazena as peças restantes
        self.rest = []

        # Vetor que mostra os valores nas bordas
        self.edges = []

        # Variável que identifica a rodada atual
        self.round = 1
    
    def data(self):
        return {
            'Rodada': self.round,
            'Field': self.field,
            'Edges': self.edges
        }