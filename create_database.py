import json
import numpy as np
from numpy.lib.scimath import sqrt
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('database') if isfile(join('database', f))]
print(onlyfiles)

def distance(array1, array2):
    dist = (array1[0] - array2[0])**2 + (array1[1] - array2[1])**2 + (array1[2] - array2[2])**2 + (array1[3] - array2[3])**2 + (array1[4] - array2[4])**2 + (array1[5] - array2[5])**2 + (array1[6] - array2[6])**2 + (array1[7] - array2[7])**2 + (array1[8] - array2[8])**2 + (array1[9] - array2[9])**2 + (array1[10] - array2[10])**2
    dist = sqrt(dist)
    print(dist)

def can_play(hand, edge):
    for piece in hand:
            if piece[0] == edge or piece[1] == edge:
                return True

def most_common(hand):
    cont = [0,0,0,0,0,0,0]
    values = []
    for piece in hand:
        cont[piece[0]] += 1
        cont[piece[1]] += 1
    cont = np.array(cont)
    while len(values) < 7:
        result = np.where(cont == np.max(cont))
        values.append(np.max(result[0]))
        cont[np.max(result[0])] = -1
    return values

def treatment(data):

    field = data['Field']
    hand1 = data['Player1']
    hand2 = data['Player2']
    edges = data['Edges']

    # Field
    count = 0
    for i in range(len(field)):
        for ii in range(len(field[i])):
            if field[i][ii] != 0:
                count += 1

    # Edges
    edge = 0
    if can_play(hand2, edges[0]):
        edge += 1
    if can_play(hand2, edges[1]):
        edge += 1
    
    # Hands
    data = [count, len(hand1), len(hand2), edge]

    # Most Common pieces
    values = most_common(hand2)
    for i in range(7):
        data.append(int(values[i]))
    
    if edge != 0 and len(hand1) != 0 and len(hand2) != 0:
        return data
    else:
        return -1


database = []
for file in onlyfiles:
    data = open('database\\' + file, 'r')
    for linha in data:
        data = linha
    data = json.loads(data)
    games = len(data)
    for game in range(games):
        rodadas = len(data[game]['Rodadas'])
        for rodada in range(rodadas):
            dado = treatment(data[game]['Rodadas'][rodada])
            if dado != -1:
                jogo = {
                    'Dado': dado,
                    'Resultado': data[game]['Resultado']
                }
                database.append(jogo)
arquivo = open('database.json',"a")
database = json.dumps(database)
arquivo.write(database)
arquivo.close()