from requests import get, post

from settings import OAuth_TOKEN
url = "https://dialogs.yandex.net/api/v1/status"
headers = {
    'Authorization': f"OAuth {OAuth_TOKEN}"
}
response = get(url, headers=headers)
print(response.json())


# print(get('http://localhost:8080/api/news').json())
#
# id = 3
# print(get(f'http://localhost:8080/api/news/{id}').json())
#
# print(post('http://localhost:8080/api/news', json={}).json())
#
# print(post('http://localhost:8080/api/news',
#            json={'title': 'Заголовок'}).json())
#
# print(post('http://localhost:8080/api/news',
#            json={'title': 'Header',
#                  'content': 'News text',
#                  'user_id': 1,
#                  'is_private': False}).json())