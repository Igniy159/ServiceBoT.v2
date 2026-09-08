from pydantic import BaseModel, Field

class CreateBranch(BaseModel):
    """Command for create branch"""
    name: str = Field(max_length=20)

class RenameBranch(BaseModel):
    """Command for rename branch"""
    branch_id: int = Field(gt= 0)
    new_name: str = Field(max_length=20)

class ReceiveBranch(BaseModel):
    """Command for receive branch"""
    is_active: bool | None = True

class DeleteBranch(BaseModel):
    """Command for delete branch"""
    branch_id: int = Field(gt=0)
