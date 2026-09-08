from pydantic import BaseModel, Field

class CreateDepartment(BaseModel):
    """Command for create department"""
    name: str = Field(max_length=20)

class ReceiveDepartment(BaseModel):
    """Command for receive department"""
    is_active: bool | None = True

class DeleteDepartment(BaseModel):
    """Command for delete department"""
    department_id: int = Field(gt=0)
