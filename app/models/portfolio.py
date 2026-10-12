import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum
from app.core.database import Base

class AssetType(str, enum.Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    SAVINGS = "savings"
    DEBT = "debt"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ticker = Column(String, index=True, nullable=True)  # e.g., AAPL, BTC-USD
    asset_type = Column(SQLEnum(AssetType), nullable=False)
    quantity = Column(Float, nullable=False, default=0.0)
    purchase_price = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False)  # e.g., Housing, Food, Utilities
    amount = Column(Float, nullable=False)
    monthly_limit = Column(Float, nullable=True)  # Target threshold for variance warnings
    description = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
