from player import Player

class H1(Player):
    def select_piece_to_play(self, left, right):
        # Jogadas válidas
        valid_plays = []

        # Quantidade de peças de cada número
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
    def select_piece_to_play(self, left, right, field, height, width):
        # Jogadas válidas
        valid_plays = []

        # Quantidade de peças de cada número
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
    
        # Se não retorne a única peça válida e o lado pra jogar 
        else:
            return [valid_plays[0][0], valid_plays[0][1]]