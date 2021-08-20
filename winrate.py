from os import listdir
from os.path import isfile, join
import json
cont = 0
onlyfiles = [f for f in listdir('H1xR') if isfile(join('H1xR', f))]
for file in onlyfiles:
    data = open('H1xR\\' + file, 'r')
    for linha in data:
        data = linha
    data = json.loads(data)
    winner = data['Winner']
    if winner == 1:
        cont += 1
print(cont)
