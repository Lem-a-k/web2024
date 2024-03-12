from requests import get, post

print(get('http://localhost:8080/api/news').json())

id = 3
print(get(f'http://localhost:8080/api/news/{id}').json())

print(post('http://localhost:8080/api/news', json={}).json())

print(post('http://localhost:8080/api/news',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:8080/api/news',
           json={'title': 'Header',
                 'content': 'News text',
                 'user_id': 1,
                 'is_private': False}).json())