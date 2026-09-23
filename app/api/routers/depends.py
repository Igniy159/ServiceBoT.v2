from collections.abc import AsyncGenerator
from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from app.models import User
from app.setting_app import setting_app


async def get_session()-> AsyncGenerator[AsyncSession,None]:
    async with setting_app.session_factory() as session:
        yield session


async def authenticate(session: AsyncSession = Depends(get_session),
                       authorization: str | None = Header(default=None))->User:
    try:
        scheme, token = authorization.split(" ", 1)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")

    user_id = jwt.decode(token)

    stmt = select(User).where(
        User.id == user_id,
        User.is_active.is_(True),)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user

