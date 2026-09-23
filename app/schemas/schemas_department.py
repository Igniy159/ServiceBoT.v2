from pydantic import BaseModel, Field, ConfigDict


class CreateDepartment(BaseModel):
    """Command for create department"""
    name: str = Field(max_length=20)

class ReceiveDepartment(BaseModel):
    """Command for receive department"""
    is_active: bool | None = True

class DeactivateDepartment(BaseModel):
    """Command for soft delete department"""
    department_id: int = Field(gt=0)

class DepartmentDTO(BaseModel):
    name: str = Field(max_length=20)
    model_config = ConfigDict(from_attributes=True)