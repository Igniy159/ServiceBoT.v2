import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import AuthorizeError
from app.models import User
from app.policy.boostrap_policy import BoostrapPolicy
from app.schemas.schemas_user import Registry, UserDTO


class RegistrationUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.boostrap = BoostrapPolicy()

    async def boostrap_admin_registry(self, cmd: Registry)->UserDTO:
        """Registry only admin if db empty"""
        if await self.boostrap.has_user_in_db(self.session):
            raise AuthorizeError('DB is not empty')
        # NOT ASYNC FUNC !!!
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(cmd.password.encode(),salt).decode()
        role_id = await self.boostrap.get_admin_id(self.session)
        new_user = User(name=cmd.name,
                        tg_id=cmd.tg_id,
                        email=cmd.email,
                        password_hash=password_hash,
                        role_id=role_id)
        self.session.add(new_user)
        await self.session.flush()
        return UserDTO(id=new_user.id,
                       name=new_user.name)
