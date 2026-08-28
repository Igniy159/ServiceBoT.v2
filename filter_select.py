from session_first_model import session, Branch
from sqlalchemy import select
from select_orm import add_branch, del_branches


def orm_operation():
    """
    .in_ -вхожение в iterable
    .not_in - не вхождение в iterable
    .like - содержит ("Мос%") подстроку
    .ilike - содержит подстроку без учета регистра
    .between - входит в интервал
    .is_ - является
    """
    res = []
    res.append(session.scalars(select(Branch).where(Branch.id.in_([1,3]))).all())
    res.append(session.scalars(select(Branch).where(Branch.id.not_in([1,2,3,4]))).all())
    return res

def find_branches(
    department_id:int=None,
    name: str=None,
    ids: list[int]=None)->list[Branch]:
    condition = []
    if department_id:
        condition.append((Branch.id == department_id))
    if name:
        condition.append((Branch.name.ilike(f'%{name}%')))
    if ids:
        condition.append(Branch.id.in_(ids))
    return session.scalars(select(Branch).where(*condition)).all()

def main():
    add_branch()
    print(find_branches())
    del_branches()


if __name__ == '__main__':
    main()
