import json


with open('xan.txt', encoding='utf-8') as fh:
    data = json.load(fh)
    print(data)