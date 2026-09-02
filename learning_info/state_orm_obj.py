from learning_info.session_first_model import session, Branch
from sqlalchemy import inspect, select, text

def check_branches():
    res = session.execute(select(Branch))
    return res.scalars().all()

def main():
    branch = Branch(name='Ереван')
    state = inspect(branch)
    print(state.transient, 'временный, только созданный объект, вне сессии')
    #добавляем в сессию
    session.add(branch)
    print(state.pending, 'Добавленный в сессию, в ожидании')
    session.flush()
    print(state.persistent,'Устойчивый объект. Отправлен в БД. Коммита еще нет')
    session.commit()
    session.close()
    print(state.detached, 'Объект надежно записан после commit. Перешел после закрытия session')
    result = session.execute(select(Branch))
    branches = result.scalars().all()
    print(result, 'res')
    for k in branches:
        print(k.id, k.name, 'branch')
    print(state)
    session.execute(text("DELETE FROM branches"))
    print(check_branches(),'таблица очищена')

if __name__ == '__main__':
    main()
