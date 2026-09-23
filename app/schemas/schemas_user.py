from typing import Optional
from pydantic import BaseModel, Field

class Registry(BaseModel):
    name: str = Field(max_length=20)
    email: str = Field(max_length=50)
    password: str = Field(max_length=50)
    tg_id: Optional[int] = Field(default=None, gt=0)

class UserDTO(BaseModel):
    name: str = Field(max_length=20)
    role_name: Optional[str] = Field(default=None,max_length=20)
    department_name: Optional[str] = Field(default=None,max_length=20)
    branch_name: Optional[str] = Field(default=None,max_length=20)
    email: Optional[str] = Field(default=None,max_length=50)
    tg_id: Optional[int] = Field(default=None, gt=0)

class LoginData(BaseModel):
    email: str = Field(max_length=50)
    password: str = Field(max_length=50)


class CreateTgUser(BaseModel):
    """Command for create new user from TG entry"""
    name: str = Field(max_length=20)
    tg_id: int = Field(gt=0)
    role_id: int = Field(gt=0)
    branch_id: int| None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)

class AddLinkTg(BaseModel):
    user_id: int = Field(gt=0)
    tg_id: int = Field(gt=0)

class ActivateUser(BaseModel):
    """Command for soft delete user"""
    user_id: int = Field(gt=0)

class DeactivateUser(BaseModel):
    """Command for soft delete user"""
    user_id: int = Field(gt=0)

class RenameUser(BaseModel):
    """Command for rename user"""
    user_id: int = Field(gt=0)
    new_name: str = Field(max_length=20)

class ChangeUser(BaseModel):
    """
    Command for change user.
    For business reasons, it is advisable to provide complete data
    """
    user_id: int = Field(gt=0)
    role_id: int = Field(gt=0)
    department_id: int | None = Field(default=None, gt=0)
    branch_id: int | None = Field(default=None, gt=0)

class ReceiveUser(BaseModel):
    """ Command for get use with optional filter"""
    user_id: int | None = Field(default=None, gt=0)
    tg_id: int | None = Field(default=None, gt=0)
    branch_id: int | None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)
    role_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = True
    limit: int = Field(default=50, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
