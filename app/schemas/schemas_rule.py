from pydantic import BaseModel, Field, ConfigDict
from app.enums import ClassRule

class CreateRule(BaseModel):
    """Create new rule from system"""
    class_rule: ClassRule
    name: str = Field(max_length=20)
    department_id: int = Field(gt=0)

class DeleteRule(BaseModel):
    rule_id: int = Field(gt=0)

class RuleDTO(BaseModel):
    class_rule: ClassRule
    name: str = Field(max_length=20)

    model_config = ConfigDict(from_attributes=True)
