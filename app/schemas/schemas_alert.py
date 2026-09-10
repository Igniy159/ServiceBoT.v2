from pydantic import BaseModel, Field


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
    target_id: int | None = Field(default=None,gt=0)

    limit: int = Field(default=50, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
