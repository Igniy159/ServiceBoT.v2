from sqlalchemy.orm import Session

from app.model_user import User
from app.setting_app import setting_app

users = [User(name='Alice'),
         User(name='Bob'),
         User(name='Charlie')]

def add_user(session: Session,
             users: list[User]):
    session.add_all(users)
    session.commit()
    print('Добавлены тестовые пользователи')


def main():
    add_user(setting_app.session, users)

if __name__ == '__main__':
    main()
