from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.portfolio import AssetType

class AssetBase(BaseModel):
    name: str
    ticker: Optional[str] = None
    asset_type: AssetType
    quantity: float = Field(gt=0, description="Quantity must be greater than zero")
    purchase_price: float = Field(ge=0, description="Purchase price must be non-negative")

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    category: str
    amount: float = Field(gt=0)
    monthly_limit: Optional[float] = None
    description: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
