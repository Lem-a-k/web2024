from flask import Flask, url_for, request, render_template

app = Flask(__name__)

params = {'user_name': 'Вася',
          }


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", css_url=f"{url_for('static', filename='css/style.css')}",
                           title="Главная страница", user_name=params.get('user_name', 'Аноним'))


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


@app.route('/form_sample', methods=['POST', 'GET'])
def form_sample():
    if request.method == 'GET':
        return f'''<!doctype html>
                        <html lang="en">
                          <head>
                            <meta charset="utf-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                            <link rel="stylesheet"
                            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                            integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                            crossorigin="anonymous">
                            <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                            <title>Пример формы</title>
                          </head>
                          <body>
                            <h1>Форма для регистрации в суперсекретной системе</h1>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                    <input type="password" class="form-control" id="password" placeholder="Введите пароль" name="password">
                                    <div class="form-group">
                                        <label for="classSelect">В каком вы классе</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>8</option>
                                          <option>9</option>
                                          <option>10</option>
                                          <option>11</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="about">Немного о себе</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готов быть добровольцем</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Записаться</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        try:
            print(request.form['email'])
            print(request.form['password'])
            print(request.form['class'])
            print(request.form['file'])
            print(request.form['about'])
            print(request.form['accept'])
            print(request.form['sex'])
        except Exception as e:
            print(e)
        return "Форма отправлена"


@app.route('/test_carousel')
def return_carousel():
    if 'pics' not in params:
        params['pics'] = [(f"{url_for('static', filename='img/1.jpeg')}", "first"),
                          (f"{url_for('static', filename='img/2.jpeg')}", "second"),
                          (f"{url_for('static', filename='img/3.jpeg')}", "third")
                          ]
    return render_template('test_carousel.html', title='Карусель', pics=params['pics'])


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')
