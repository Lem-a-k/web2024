import logging

import pymorphy3
from flask import Flask, url_for, request, render_template, session, redirect, make_response, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms import StringField, TextAreaField
from werkzeug.utils import secure_filename

from data import db_session, news_api
from fill_db import fill_users, get_user
from data.users import User
from data.news import News

from settings import OAuth_TOKEN
from geocoder import get_city_map_url
from images import upload_picture

DB_NAME = 'site'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

logging.basicConfig(level=logging.INFO)

settings = {'user_name': 'Вася',
            }

sessionStorage = {}

morph = pymorphy3.MorphAnalyzer()

@app.route('/')
@app.route('/index')
def index():
    session['visits_count'] = session.get('visits_count', 0) + 1
    print(session['visits_count'])
    return render_template("index.html",
                           visits=session['visits_count'],
                           css_url=f"{url_for('static', filename='css/style.css')}",
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


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')


@app.route('/news', methods=['GET', 'POST'])
def add_news():
    form = NewsForm()
    current_user = get_user(DB_NAME)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_news.html', title='Добавление новости',
                           form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


things = ['слона', 'кролика', 'зебру', 'кенгуру', 'льва']

@app.route('/post', methods=['GET', 'POST'])
def alice_main():
    if request.method == 'GET':
        
        return "post"
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    
    logging.info(f'Response:  {response!r}')
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'stage': 0,
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = f'Привет! Купи {things[sessionStorage[user_id]["stage"]]}!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if any(x in req['request']['original_utterance'].lower() for x in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо'
    ]):
        res['response']['text'] = f'{things[sessionStorage[user_id]["stage"]].capitalize()} можно найти на Яндекс.Маркете!'
        
        sessionStorage[user_id]['stage'] += 1
        if len(things) == sessionStorage[user_id]['stage']:
          res['response']['end_session'] = True
        else:
          res['response']['text'] += f' А теперь купи {things[sessionStorage[user_id]["stage"]]}.'
          sessionStorage[user_id]['suggests'] = [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        return
    map_url = get_city_map_url(req['request']['original_utterance'])
    result = upload_picture(map_url)
    im_id = result['image']['id']
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['title'] = f"Это {req['request']['original_utterance']}"
    res['response']['card']['image_id'] = im_id          
            
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {things[sessionStorage[user_id]['stage']]}!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session
    
    nf = morph.parse(things[sessionStorage[user_id]['stage']])[0].normal_form
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={nf}",
            "hide": True
        })

    return suggests


def main():
    db_session.global_init(f"db/{DB_NAME}.db")
    fill_users(DB_NAME)
    app.register_blueprint(news_api.blueprint)
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
