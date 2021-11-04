from player import Player
from operator import itemgetter
import numpy as np
import json

class Random(Player):
    def __init__(self):
        super().__init__()
        self.name = "Random"
    
    def select_piece_to_play(self, left, right):
        # Retorna a primeira peça que pode ser jogada e a borda a ser jogada
        for piece in self.hand:
            if piece[0] == left[0]:
                return [piece, 'Left']
            if piece[1] == left[0]:
                return [piece, 'Left']
            if piece[0] == right[0]: 
                return [piece, 'Right']
            if piece[1] == right[0]:
                return [piece, 'Right']

class H1(Player):
    def __init__(self):
        super().__init__()
        self.name = "H1"

    def select_piece_to_play(self, left, right):
        valid_plays = []
        backups = [0,0,0,0,0,0,0]

        # Peça com mais backup, quantidade de backup da peça, soma dos valores da peça, lado para jogar
        biggest = [[],0,0,'']

        # Percorre a mão
        for i in range(len(self.hand)):
            # Verificando peças com mais backup
            backups[self.hand[i][0]] += 1
            backups[self.hand[i][1]] += 1

        # Verificando possiveis jogadas
        for piece in self.hand:
            if piece[0] == left[0]: 
                valid_plays.append([piece, 'Left'])
            elif piece[0] == right[0]:
                valid_plays.append([piece, 'Right'])
            elif piece[1] == left[0]:
                valid_plays.append([piece, 'Left'])
            elif piece[1] == right[0]:
                valid_plays.append([piece, 'Right'])
        
        # Se houver mais de uma peça válida
        if len(valid_plays)>1:
            for j in range(len(valid_plays)):
                # Métrica pra verificar maior backup
                backup = (backups[valid_plays[j][0][0]]+backups[valid_plays[j][0][1]])
                # Métrica de desempate com a maior peça
                better = valid_plays[j][0][0] + valid_plays[j][0][1]

                # Se empatar no backup pegar a maior peça
                if backup == biggest[1]:
                    if better > biggest[2]:
                        biggest = [valid_plays[j][0], backup, better, valid_plays[j][1]]
                elif backup > biggest[1]:
                    biggest = [valid_plays[j][0], backup, better, valid_plays[j][1]]
            return [biggest[0], biggest[3]]
    
        # Se não retorne a única peça válida e o lado pra jogar 
        else:
            return [valid_plays[0][0], valid_plays[0][1]]

class H2(Player):
    def __init__(self):
        super().__init__()
        self.name = "H2"

    def select_piece_to_play(self, left, right, field, height, width):
        valid_plays = []
        backups = [0,0,0,0,0,0,0]

        # Peça com mais backup, quantidade de backup da peça, soma dos valores da peça, lado para jogar
        biggest = [[],0,0,'']

        # Percorre a mão
        for i in range(len(self.hand)):
            # Verificando peças com mais backup
            backups[self.hand[i][0]] += 1
            backups[self.hand[i][1]] += 1
        
        # Percorre o campo
        for line in range(int(height/70)):
            for column in range(int(width/70)):
                if field[line][column] != 0:
                    # Verificando peças com mais backup
                    backups[field[line][column][0][0]] += 1
                    backups[field[line][column][0][1]] += 1

        # Verificando possiveis jogadas
        for piece in self.hand:
            if piece[0] == left[0]: 
                valid_plays.append([piece, 'Left'])
            elif piece[0] == right[0]:
                valid_plays.append([piece, 'Right'])
            elif piece[1] == left[0]:
                valid_plays.append([piece, 'Left'])
            elif piece[1] == right[0]:
                valid_plays.append([piece, 'Right'])
        
        # Se houver mais de uma peça válida
        if len(valid_plays)>1:
            for j in range(len(valid_plays)):
                # Métrica pra verificar maior backup
                backup = (backups[valid_plays[j][0][0]]+backups[valid_plays[j][0][1]])
                # Métrica de desempate com a maior peça
                better = valid_plays[j][0][0] + valid_plays[j][0][1]

                # Se empatar no backup pegar a maior peça
                if backup == biggest[1]:
                    if better > biggest[2]:
                        biggest = [valid_plays[j][0], backup, better, valid_plays[j][1]]
                elif backup > biggest[1]:
                    biggest = [valid_plays[j][0], backup, better, valid_plays[j][1]]
            return [biggest[0], biggest[3]]
    
        # Se não, retorne a única peça válida e o lado pra jogar 
        else:
            return [valid_plays[0][0], valid_plays[0][1]]

class KNN(Player):

    def __init__(self):
        super().__init__()
        self.name = "K-NN"
        self.k = 10

        # Buscando informações do banco de dados
        data = open('database.json', 'r') 
        for line in data:
            data = line
        data = json.loads(data)
        self.database = data
        
    # Converte as informações recebidas no formato do vetor desejado
    def converter(self, field, temporary_hand, oponent_hand, edges):

        # Verifica quantas peças existem no campo
        count = 1
        for i in range(len(field)):
            for ii in range(len(field[i])):
                if field[i][ii] != 0:
                    count += 1

        # Verifica em quantas bordas é possivel jogar
        edge = 0
        for piece in temporary_hand:
                if piece[0] == edges[0] or piece[1] == edges[0]:
                    edge += 1
        for piece in temporary_hand:
                if piece[0] == edges[1] or piece[1] == edges[1]:
                    edge += 1
        
        # Verifica quantas peças na mão de cada jogador
        data = [count, len(temporary_hand), len(oponent_hand), edge]

        # Contador para verificar as peças mais comuns
        cont = [0,0,0,0,0,0,0]
        for piece in temporary_hand:
            cont[piece[0]] += 1
            cont[piece[1]] += 1
        
        # Convertendo para um array numpy
        cont = np.array(cont)

        # Salvando os valores na ordem
        values = []
        while len(values) < 7:
            result = np.where(cont == np.max(cont))
            values.append(np.max(result[0]))
            cont[np.max(result[0])] = -1
        
        # Adicionando as peças mais comuns em ordem
        for i in range(7):
            data.append(int(values[i]))
        
        return data
    
    def win_rate(self, array):
        distances = []

        # Calculando a distância entre o vetor de estado e todos os dados de estado encontrados
        for data in self.database:
            neighbor = data['Dado']
            distance = (neighbor[0] - array[0])**2 + (neighbor[1] - array[1])**2 + (neighbor[2] - array[2])**2 + (neighbor[3] - array[3])**2 + (neighbor[4] - array[4])**2 + (neighbor[5] - array[5])**2 + (neighbor[6] - array[6])**2 + (neighbor[7] - array[7])**2 + (neighbor[8] - array[8])**2 + (neighbor[9] - array[9])**2 + (neighbor[10] - array[10])**2
            distance = np.lib.scimath.sqrt(distance)
            resultado = data['Resultado']
            distances.append([distance, resultado])
        
        # Ordenando pela distância euclidiana
        distances = sorted(distances, key=itemgetter(0))

        # Verificando os rótulos dos K vizinhos mais próximos e armazenando a taxa de vitória
        win_rate = 0
        for i in range(self.k):
            if distances[i][1] == 2:
                win_rate +=1
        
        # Retorna a taxa de vitória
        return win_rate

    def select_piece_to_play(self, left, right, field, opponent_hand):
        valid_plays = []
        temporary_hand = []
        temporary_plays = []

        # Verificando possiveis jogadas
        for piece in self.hand:

            # Salvando a mão temporária
            temporary_hand.append(piece)
            if piece[0] == left[0]: 
                valid_plays.append([piece, 'Left'])
            elif piece[0] == right[0]:
                valid_plays.append([piece, 'Right'])
            elif piece[1] == left[0]:
                valid_plays.append([piece, 'Left'])
            elif piece[1] == right[0]:
                valid_plays.append([piece, 'Right'])

        # Avaliar cada jogada válida
        for piece_edge in valid_plays:
            if piece_edge[1] == 'Left':

                # Remove a peça da mão para simular a jogada
                temporary_hand.remove(piece_edge[0])

                # Verifica qual valor assumiria a borda
                if piece_edge[0][0] == left[0]:
                    edge = piece_edge[0][1]
                elif piece_edge[0][1] == left[0]:
                    edge = piece_edge[0][0]
                
                # Converte as informações usadas para simular o estado de jogo em um vetor
                array = self.converter(field, temporary_hand, opponent_hand, [edge, right[0]])
 
            elif piece_edge[1] == 'Right':
                # Remove a peça da mão para simular a jogada
                temporary_hand.remove(piece_edge[0])

                # Verifica qual valor assumiria a borda
                if piece_edge[0][0] == right[0]:
                    edge = piece_edge[0][1]
                elif piece_edge[0][1] == right[0]:
                    edge = piece_edge[0][0]
                
                # Converte as informações usadas para simular o estado de jogo em um vetor
                array = self.converter(field, temporary_hand, opponent_hand, [left[0], edge])

            # Retorna a taxa de vitória do vetor convertido
            win_rate = self.win_rate(array)

            # Salva a taxa de vitória da jogada simulada
            temporary_plays.append([piece_edge, win_rate])

            # Retorna a peça para a mão para a próxima simulação
            temporary_hand.append(piece_edge[0])
        
        # Ordenar as jogadas pela taxa de vitória
        temporary_plays = sorted(temporary_plays, key=itemgetter(1), reverse=True)

        # Retornar a melhor jogada
        return temporary_plays[0]