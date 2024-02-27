from data.users import User
from data import db_session


def fill_users(DB_NAME):
    db_session.global_init(f"db/{DB_NAME}.db")
    user = User()
    user.name = "Пользователь 1"
    user.email = "email@email.ru"
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()

if __name__ == "__main__":
    pass