'''
Implementação:

Coleta de dados:

Estrutura da rede:

pm = peças na minha mão
po = peças na mão do oponente
pc = peças no campo

q+C ... q-C = peça mais comum (ordem de aparecimento e o desempate é o id da peça)

qj = quantas bordas disponíveis para jogar

pm | po | pc | q+C |   |   |   |   |   | q-C | qj

KNN

distancia euclidiana do estado atual para do banco de dados
'''

import sklearn
from sklearn.neighbors import KNeighborsClassifier
import json

def treatment(field, hand1, hand2, edges):
    pc = field
    po = hand2
    pm = hand1

data = open('2021_08_05_00_41_16_844.json', 'r')

for linha in data:
    data = linha
data = json.loads(data)
print(data[0]['Rodadas'][0])

knn = KNeighborsClassifier(n_neighbors=10)
knn.fit()