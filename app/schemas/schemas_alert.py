from datetime import datetime
from pydantic import BaseModel, Field
from app.enums import ClassRule


class CreateAlert(BaseModel):
    """Command for create alert"""
    rule_id: int = Field(gt=0)
    branch_id: int | None = Field(default=None, gt=0)
    comment: str | None = Field(default=None,max_length=100)

class ReceiveAlerts(BaseModel):
    """Command for get alerts with optional filters"""
    alert_id: int | None = Field(default=None,gt=0)
    creator_id: int | None = Field(default=None,gt=0)
    branch_id: int | None = Field(default=None,gt=0)
    department_id: int | None = Field(default=None, gt=0)
    class_rule: ClassRule | None = None

    limit: int = Field(default=50, gt=0, le=100)
    offset: int = Field(default=0, ge=0)

    created_from: datetime  | None = None
    created_to: datetime | None = None

class AlertDTO(BaseModel):
    rule_name: str = Field(max_length=20)
    creator_name: str = Field(max_length=20)
    branch_name: str = Field(max_length=20)
    department_name: str = Field(max_length=20)
    comment: str | None = Field(default=None,max_length=100)
    created_at: datetime
