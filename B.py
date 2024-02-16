# http, json

# задача "get 2 + 2" из урока "WEB. Работа с протоколом HTTP"

import json
import requests

with open('settings.json') as in_file:
    settings = json.load(in_file)  # хост, порт и другие данные

url = f"http://{settings['host']}:{settings['port']}"
response = requests.get(url).json()

print(response)
# преобразование ответа сервера, сортировка, фильтарция
