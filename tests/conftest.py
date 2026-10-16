import asyncio
import sys
from dataclasses import dataclass

import pytest

from app.models import Branch, User

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

class FakeBranches:
    def __init__(self):
        self.dragon = Branch(name='Летящий дракон')
        self.boar = Branch(name='Раненный вепрь')
        self.pony = Branch(name='Гарцующий пони')
        self.wolf = Branch(name='Старый волк')

    def all(self)-> list[Branch]:
        return [self.dragon,
                self.boar,
                self.pony,
                self.wolf]

@pytest.fixture
def branches():
    return FakeBranches().all()

@dataclass
class FakeUsers:
    admin = User(name='Великий АДМИН',tg_id=8752047609,role_id=1)
    owner = User(name='Владыка Системы', tg_id= 38923424542, role_id=2)
    manager = User(name='Управляющий',tg_id=2934632345, role_id=3)
    employee = User(name='Пользователь', tg_id=234234446354, role_id=4)
    ars = User(name='Великий исправитель',tg_id=2422434553, role_id=5,department_id=4)
    security = User(name='Страж порядка', tg_id= 134112352313, role_id=6,department_id=2)
    it = User(name='Повелитель молний', tg_id=13412432213, role_id=7, department_id=5)
    supply = User(name='Доставляющий грузы', tg_id=134344537313, role_id=8, department_id=6)
    accountant = User(name='Считающий золото', tg_id=671387533, role_id=9, department_id=7)
    warehouse = User(name='Хранящий блага', tg_id=987646847313, role_id=10, department_id=8)
    marketing = User(name='Возглашающий истину', tg_id=21242531, role_id=11, department_id=9)
    service = User(name='Умиротворитель приходящих', tg_id=34562847313, role_id=12, department_id=10)
    hr = User(name='Нанимающий адептов', tg_id=4245233847313, role_id=13, department_id=3)

    def all(self)->list[User]:
        return [self.admin,
                self.owner,
                self.manager,
                self.employee,
                self.ars,
                self.supply,
                self.security,
                self.it,
                self.accountant,
                self.warehouse,
                self.marketing,
                self.service,
                self.hr
                ]

@pytest.fixture
def all_users():
    return FakeUsers().all()