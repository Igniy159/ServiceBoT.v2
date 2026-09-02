from sqlalchemy import select
from learning_info.select_orm import add_branch, del_branches
from session_first_model import User, session, Roles


def add_users():
    users = [User(name='Alex',branch_id=1, depart_id=None, role=Roles.EMPLOYEE),
             User(name='Petr',branch_id=2, depart_id=None, role=Roles.MANAGER)]
    session.add_all(users)



def main():
    add_branch()
    add_users()
    print(session.scalars(select(User)).all())

    del_branches()
if __name__ == '__main__':
    main()