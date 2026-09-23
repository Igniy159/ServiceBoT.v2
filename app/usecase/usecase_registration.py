import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.policy.boostrap_policy import BoostrapPolicy
from app.schemas.schemas_user import Registry, UserDTO


class RegistrationUseCase:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.boostrap = BoostrapPolicy(session)

    async def public_registry(self, cmd: Registry)->UserDTO:
        # NOT ASYNC FUNC !!!
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(cmd.password.encode(),salt).decode()
        role_id = None
        if not await self.boostrap.has_user_in_db():
            role_id = await self.boostrap.get_owner_id()
        new_user = User(name=cmd.name,
                        tg_id=cmd.tg_id,
                        email=cmd.email,
                        password_hash=password_hash,
                        role_id=role_id)
        self.session.add(new_user)
        await self.session.flush()
        return UserDTO(name=new_user.name,
                       email=new_user.email,
                       tg_id=new_user.tg_id)
