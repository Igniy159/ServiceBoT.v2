from pydantic import BaseModel, Field, EmailStr

class CreateTgUser(BaseModel):
    """Command for create new user from TG entry"""
    name: str = Field(max_length=20)
    tg_id: int = Field(gt=0)
    role_id: int = Field(gt=0)
    branch_id: int| None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)

class CreateWebUser(BaseModel):
    """Command for create new user from WEB entry"""
    name: str = Field(max_length=20)
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)
    role_id: int = Field(gt=0)
    branch_id: int| None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)

class AddTgId(BaseModel):
    tg_id: int = Field(gt=0)

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
