from data.users import User
from data import db_session

from settings import login as loginVK, password as passVK


def get_user(DB_NAME):
    db_session.global_init(f"db/{DB_NAME}.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).filter(User.email == "email@email.ru").first()


def fill_users(DB_NAME):
    db_session.global_init(f"db/{DB_NAME}.db")
    db_sess = db_session.create_session()

    user = User()
    user.name = "Пользователь 1"
    user.email = "email@email.ru"

    user_e = db_sess.query(User).filter(User.email == user.email).first()
    print(user_e)
    if user_e is None:
        db_sess.add(user)
        db_sess.commit()


if __name__ == "__main__":
    pass
