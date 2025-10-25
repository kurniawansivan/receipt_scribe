from pydantic import BaseModel
from typing import List, Optional
from datetime import date as Date

class ExpenseItem(BaseModel):
    description: str
    amount: float

class ExpenseBase(BaseModel):
    vendor_name: Optional[str] = None
    date: Optional[Date] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    items: Optional[List[ExpenseItem]] = []

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    
    class Config:
        from_attributes = True

class ExpenseSummary(BaseModel):
    total_expenses: float
    expense_count: int
    recent_expenses: List[ExpenseResponse]

class UploadResponse(BaseModel):
    success: bool
    expense_id: Optional[int] = None
    message: Optional[str] = None
    error: Optional[str] = None