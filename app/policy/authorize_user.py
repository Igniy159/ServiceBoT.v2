from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from app.errors import AuthorizeError
from app.models import User, Role, Permission


class Authorize:
    def __init__(self, session: AsyncSession, actor: User):
        self.session = session
        self.actor = actor
        self.permissions: set[Permission] | None = None

    async def load_permissions(self):
        stmt = Select(Role.permissions).where(Role.id == self.actor.role_id)
        result = await self.session.execute(stmt)
        permissions = list(result.scalars().all())
        self.permissions = {p.name for p in permissions}

    def check(self, permission: str):
        permissions = self.permissions
        if permissions is None:
            raise AuthorizeError("Permissions have not been loaded")
        if permission not in permissions:
            raise AuthorizeError(f'User can not use this action {permission}')

