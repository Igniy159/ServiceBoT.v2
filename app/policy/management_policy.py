from app.errors import AuthorizeError
from app.models import Role


class ManagementPolicy:

    @staticmethod
    def check_management(actor_role: Role,
            desired_role:Role):
        if actor_role.name == 'Владелец' and desired_role.name == 'Владелец':
            raise AuthorizeError
        if actor_role.name == 'Админ' and desired_role.name == 'Админ':
            raise AuthorizeError
        if actor_role.name == 'Управляющий филиала' and desired_role.name != 'Сотрудник филиала':
            raise AuthorizeError
