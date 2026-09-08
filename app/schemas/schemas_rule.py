from pydantic import BaseModel, Field
from app.enums import KindRule, ClassRule

class CreateRule(BaseModel):
    """Create new rule from system"""
    kind_rule: KindRule
    class_rule: ClassRule
    name: str = Field(max_length=20)
    department_id: int = Field(gt=0)

class DeleteRule(BaseModel):
    rule_id: int = Field(gt=0)
