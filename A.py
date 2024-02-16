# csv, json + структуры данных и встроенные функции

import csv
import json

with open('test.csv') as in_file:
    reader = csv.DictReader(in_file, delimiter=';')
    # другая логика
    lines = {line['name']: [line['color'], line['text'][:5]]
             for line in reader if int(line['age']) > 4}
# print(lines)
# дополнительные преобразования
with open('test.json', 'w') as out_file:
    json.dump(lines, out_file)
