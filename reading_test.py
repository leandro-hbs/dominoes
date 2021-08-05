import json

data = open('2021_08_05_00_41_16_844.json', 'r')
for linha in data:
    data = linha
data = json.loads(data)
print(data[0]['Rodadas'][0])