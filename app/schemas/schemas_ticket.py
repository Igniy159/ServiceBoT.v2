from pydantic import BaseModel, Field
from app.enums import Severity, State
from datetime import datetime

class CreateTicket(BaseModel):
    """ Command for create ticket."""
    rule_id: int = Field(gt=0)
    severity: Severity
    branch_id: int | None = Field(default=None, gt=0)
    comment: str | None = Field(default=None, max_length=100)
    file_id: str | None = None


class ChangeStateTicket(BaseModel):
    """Command for reject ticket"""
    ticket_id: int = Field(gt=0)
    new_state: State
    comment: str = Field( max_length=100)

class ReceiveTicket(BaseModel):
    """ Command for get ticket with optional filter"""
    ticket_id: int | None = Field(default=None, gt=0)
    branch_id: int | None = Field(default=None, gt=0)
    department_id: int | None = Field(default=None, gt=0)
    creator_id: int | None = Field(default=None, gt=0)
    state: State | None = None

    created_from: datetime  | None = None
    created_to: datetime | None = None

    limit: int = Field(default=50, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
