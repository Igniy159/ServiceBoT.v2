from sqlalchemy import select, text
from sqlalchemy.engine import Result
from session_first_model import Branch, session


def add_branch():
    branches = [Branch(name='Москва'), Branch(name='СПБ'), Branch(name='Казань'), Branch(name='Москва'), Branch(name='Тбилиси')]
    session.add_all(branches)
    session.commit()
    session.close()

def get_result_select()-> Result:
    return session.execute(select(Branch))

def get_all_branches():
    result = session.execute(select(Branch))
    return result.all()

def get_scalar_branch():
    result = session.execute(select(Branch))
    return result.scalars()

def get_branches()-> list[Branch]:
    result = session.execute(select(Branch))
    return result.scalars().all()
def get_branches_2()->list[Branch]:
    return session.scalars(select(Branch)).all()

def get_names()-> list[str]:
    return session.scalars(select(Branch.name)).all()

def select_option():
    session.scalars(select(Branch).where(Branch.id == 3))
    session.scalars(select(Branch).order_by(Branch.id.desc()))
    session.scalars(select(Branch).limit(2))

def del_branches():
    session.execute(text('DELETE FROM branches'))
    session.commit()

def main():
    add_branch()
    print(get_result_select(), 'результат select')
    print()
    print(get_all_branches(), 'результат select.all')
    print()
    print(get_scalar_branch(), 'результат select.scalars')
    print()
    print(get_branches(), 'результат select.scalars.all')
    print(get_branches_2(), 'другой синтаксис')
    print()
    print(get_names(), 'SELECT name FROM branches')
    del_branches()
