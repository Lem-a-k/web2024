from flask import Flask, url_for, request, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from data import db_session
from fill_db import fill_users
from data.users import User
from data.news import News

DB_NAME = 'site'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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


@app.route('/users_page')
def return_sample_page():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    print(users)
    return render_template('users_page.html', title='Список польователей', users=users)


@app.route('/avatar', methods=['POST', 'GET'])
def avatar():
    if request.method == 'POST':
        f = request.files['file']
        settings["avatar_file"] = f.filename
        f.save(f'static/img/{f.filename}')

    params = {'title': 'Выбор аватара!!!'}
    if 'avatar_file' in settings:
        params['avatar'] = url_for('static', filename=f"img/{settings['avatar_file']}")
    return render_template("avatar.html", **params)


class AvatarForm(FlaskForm):
    file = FileField('Файл wtf', validators=[DataRequired()])
    submit = SubmitField('Загрузить wtf')


@app.route('/avatar2', methods=['POST', 'GET'])
def avatar2():
    form = AvatarForm()
    if form.validate_on_submit():
        print(form.file.data.filename, secure_filename(form.file.data.filename))
        avatar_name = secure_filename(form.file.data.filename)
        settings["avatar_file"] = avatar_name
        form.file.data.save(f'static/img/{avatar_name}')

    params = {'title': 'Выбор аватара wtf',
              'form': form}
    if 'avatar_file' in settings:
        params['avatar'] = url_for('static', filename=f"img/{settings['avatar_file']}")
    return render_template("avatar2.html", **params)


@app.route('/test_carousel')
def return_carousel():
    if 'pics' not in settings:
        settings['pics'] = [(f"{url_for('static', filename='img/1.jpeg')}", "first"),
                            (f"{url_for('static', filename='img/2.jpeg')}", "second"),
                            (f"{url_for('static', filename='img/3.jpeg')}", "third")
                            ]
    return render_template('test_carousel.html', title='Карусель', pics=settings['pics'])


def main():
    db_session.global_init(f"db/{DB_NAME}.db")
    fill_users(DB_NAME)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
