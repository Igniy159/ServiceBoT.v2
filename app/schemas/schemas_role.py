from pydantic import BaseModel, Field
from app.enums import ClassRule
from app.models import Permission


class CreateRole(BaseModel):
    """Create new role from system"""
    name: str = Field(max_length=20)
    department_id: int = Field(gt=0)
    need_branch: bool
    need_department: bool
    responsibilities: list[ClassRule]
    permissions: list[Permission]
