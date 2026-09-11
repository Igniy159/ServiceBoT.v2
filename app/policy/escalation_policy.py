from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app import User
from app.enums import State
from app.errors import ResourceNotFound
from app.models import Rule
from app.policy.authorize_user import Authorize
from app.schemas.schemas_ticket import CreateTicket
