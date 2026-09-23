"""preset_rule

Revision ID: 2a7f34bd0736
Revises: 08e502f16004
Create Date: 2026-09-21 05:10:10.081961

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.enums import KindRule, ClassRule

def matrix_rule():
    rules = [{
    'kind': KindRule.ALERT,
    'class_rule': ClassRule.CRITICAL_ALERTS,
    'rules': ['Нет электричества','Нет интернета','Проверка от гос органов','Нет воды'],
    'target_name': "Руководство"
    },
    {'kind': KindRule.ALERT,
    'class_rule': ClassRule.SECURITY_ALERTS,
    'rules': ['Уведомление о краже','Уведомление о агрессии',
              'Проблема с сигнализацией','Потерялись ключи'],
    'target_name': "Служба безопасности"
    },
    {'kind': KindRule.ALERT,
    'class_rule': ClassRule.HR_ALERTS,
    'rules': ['Не хватает персонала','Стажер не пришёл',
                 'Проблемы с графиком','Конфликт в команде'],
    'target_name': "HR отдел"
    },
    {'kind': KindRule.ALERT,
    'class_rule': ClassRule.CASH_ALERTS,
    'rules':['Возврат средств','Ошибка в отчете', 'Расхождение в кассе'],
    'target_name': "Бухгалтерия"
    },
    {'kind': KindRule.ALERT,
    'class_rule': ClassRule.SERVICE_ALERTS,
    'rules':['Жалоба от гостя','Конфликт с гостем','Просьба связаться'],
    'target_name': "Сервис менеджер"
    },
    {'kind': KindRule.REQUEST,
    'class_rule': ClassRule.STORE_REQUEST,
    'rules':['Свежие товары для бара','Расходники для бара',
            'Напитки и кофе для бара', 'Расходники для продажи',
            'Бытовая химия', 'Канцтовары',
            'Закончилось молоко', 'Закончилось кофе', 'Закончилась позиция'],
    'target_name': "Склад"
    },
    {'kind': KindRule.REQUEST,
    'class_rule': ClassRule.INVENTORY_REQUEST,
    'rules':['Посуда для гостей', 'Приборы для гостей',
             'Ценникодержатели','Инвентарь для выпечки',
             'Инвентарь для персонала', 'Чистящее оборудование', 'Униформа'],
    'target_name': "Отдел снабжения"
    },
    {'kind': KindRule.REQUEST,
    'class_rule': ClassRule.MARKETING_REQUEST,
    'rules':['Запрос на мерч', 'Материалы для акции', 'Реклама для ТВ',
                 'Удалить старую рекламу','A3 меню', 'A4 меню', 'Постеры'],
    'target_name': "Маркетинг"
    },
    {'kind': KindRule.REQUEST,
    'class_rule': ClassRule.SECURITY_REQUEST,
    'rules':['Запрос на камеры', 'Запрос на инкассацию', 'Мешки и печати для денег'],
    'target_name': "Служба безопасности"
    },
    {'kind': KindRule.REQUEST,
    'class_rule': ClassRule.IT_REQUEST,
    'rules':['Не работает iiko', 'Не работает моноблок', 'Не работает моноблок в баре',
          'Настройка iiko','Изменить цены', 'Добавить позицию', 'Удалить позицию'],
    'target_name': "IT отдел"
    },
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.BAR_EQUIPMENT,
    'rules':['Кофемашина', 'Кофемолка',
              'Бойлер', 'Лёдогенератор','Измельчитель льда',
              'Соковыжималка', 'Блендер'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.REFRIGERATION,
    'rules':['Морозильная камера', 'Холодильник',
           'Витринный холодильник', 'Холодная витрина', 'Сухая витрина'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.ELECTRICAL,
    'rules':['Освещение', 'Розетка', 'Телевизор', 'Вывеска'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.PLUMBING,
    'rules':['Кран', 'Протечка труб', 'Раковина', 'Туалет', 'Фильтр воды'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.FURNITURE,
    'rules':['Мебель', 'Шкафчики', 'Входная дверь','Навес','Уличная мебель'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.CLIMATE,
    'rules':['Кондиционер', 'Обогреватель'],
    'target_name': "ARS отдел"},
    {'kind': KindRule.OBJECT,
    'class_rule': ClassRule.CONSUMABLE_EQUIPMENT,
    'rules':['Дозатор мыла', 'Дозатор бумаги', 'Сушилка для рук'],
    'target_name': "ARS отдел"},
    ]
    return rules

rule_table = sa.table(
    "rules",
    sa.column("kind", sa.Enum(KindRule)),
    sa.column('class_rule', sa.Enum(ClassRule)),
    sa.column('name',sa.String()),
    sa.column('target_id', sa.INTEGER())
)

# revision identifiers, used by Alembic.
revision: str = '2a7f34bd0736'
down_revision: Union[str, Sequence[str], None] = '08e502f16004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    departments = sa.table(
        "departments",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String()),
    )

    result = op.get_bind().execute(
        sa.select(
            departments.c.id,
            departments.c.name,
        )
    )

    department_ids = {
        row.name: row.id
        for row in result
    }

    rows = []

    for group in matrix_rule():
        target_id = department_ids[group["target_name"]]

        for rule_name in group["rules"]:
            rows.append({
                "kind": group["kind"].value,
                "class_rule": group["class_rule"].value,
                "name": rule_name,
                "target_id": target_id,
            })

    op.bulk_insert(rule_table, rows)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(rule_table.delete())
