from app.schemas.schemas_alert import AlertDTO
from app.schemas.schemas_ticket import TicketDTO
from app.schemas.schemas_user import UserDTO



def alert_format(alert: AlertDTO):
    msg = f"""
    Уведомление: '{alert.rule_name}'
    От филиала {alert.branch_name} | {alert.creator_name}
    Для отдела {alert.department_name}
    Комментарий: {alert.comment}
    Создан {alert.created_at}"""
    return msg


def ticket_format(ticket: TicketDTO):
    mapper_state = {
        'NEW': 'Создана',
        'CONFIRMED': 'Подтверждена',
        'IN_PROGRESS': 'В работе',
        'WAITING_EXTERNAL': 'Ожидание необходимого',
        'RESOLVED': 'Работа завершена',
        'CLOSED': 'Закрыта',
        'CANCELLED': 'Отменена'}
    mapper_severity = {'FULL_FAILURE': "Полная неисправность",
                       'PARTIAL_PROBLEM': 'Частичная поломка',
                       'MINOR_ISSUE': 'Мелкая неполадка',
                       'INCIDENT': "Срочная заявка",
                       'REQUEST': 'Регулярная заявка'}
    msg = f"""
    Заявка: '{ticket.rule_name}' | {mapper_severity[ticket.severity.name]}
    Статус: {mapper_state[ticket.state.name]}
    От {ticket.branch_name} | {ticket.creator_name}
    Для отдела {ticket.department_name}
    Комментарий: {ticket.comment}
    Создан {ticket.created_at}"""
    return msg


def user_format(user: UserDTO):
    msg = f"""
    Пользователь {user.name} | {user.tg_id}
    Роль {user.role_name}
    """
    if user.branch_name:
        msg += f'Филиал {user.branch_name}'
    if user.department_name:
        msg += f'Отдел {user.department_name}'
    return msg
