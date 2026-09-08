from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    """Command for create new user"""
    name: str = Field(max_length=20)
    tg_id: int = Field(gt=0)
    role_id: int = Field(gt=0)
    branch_id: int| None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)

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
