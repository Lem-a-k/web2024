from flask import Flask, url_for, request, render_template

app = Flask(__name__)

settings = {'user_name': 'Вася',
            }


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", css_url=f"{url_for('static', filename='css/style.css')}",
                           title="Главная страница", user_name=settings.get('user_name', 'Аноним'))


@app.route('/test')
def my_func():
    return render_template("test.html", title="Тестовая страница", data=['123', '456', 'test connection', '!'])


@app.route('/image_sample')
def image():
    return f'''<img src="{url_for('static', filename='img/owl.jpeg')}"
           alt="здесь должна была быть картинка, но не нашлась">'''


@app.route('/sample_page')
def return_sample_page():
    elems = ['Пункт первый', "Второе", "Ещё один пункт"]
    return render_template('sample_page.html', title='Особая страница', elems=elems)


@app.route('/avatar', methods=['POST', 'GET'])
def avatar():
    if request.method == 'POST':
        f = request.files['file']
        settings["avatar_file"] = f.filename
        f.save(f'static/img/{f.filename}')
        print(settings["avatar_file"])

    params = {'title': 'Выбор аватара'}
    if 'avatar_file' in settings:
        params['avatar'] = url_for('static', filename=f"img/{settings['avatar_file']}")
    return render_template("avatar.html", **params)


@app.route('/test_carousel')
def return_carousel():
    if 'pics' not in settings:
        settings['pics'] = [(f"{url_for('static', filename='img/1.jpeg')}", "first"),
                            (f"{url_for('static', filename='img/2.jpeg')}", "second"),
                            (f"{url_for('static', filename='img/3.jpeg')}", "third")
                            ]
    return render_template('test_carousel.html', title='Карусель', pics=settings['pics'])


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
