from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.portfolio import Asset, Expense
from app.schemas.portfolio import AssetCreate, AssetResponse, ExpenseCreate, ExpenseResponse
from app.services.market_service import MarketDataService

router = APIRouter()

# --- ASSETS ENDPOINTS ---
@router.post("/assets/", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    db_asset = Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/assets/", response_model=List[AssetResponse])
def get_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()

@router.get("/assets/summary/")
def get_portfolio_summary(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    total_invested = 0.0
    current_value = 0.0
    holdings = []

    for asset in assets:
        invested = asset.quantity * asset.purchase_price
        total_invested += invested
        
        # Get live price if ticker exists, else fallback to purchase price
        live_price = MarketDataService.get_current_price(asset.ticker) if asset.ticker else asset.purchase_price
        val = asset.quantity * live_price
        current_value += val
        
        holdings.append({
            "id": asset.id,
            "name": asset.name,
            "ticker": asset.ticker,
            "asset_type": asset.asset_type,
            "quantity": asset.quantity,
            "purchase_price": asset.purchase_price,
            "live_price": live_price,
            "current_value": round(val, 2),
            "gain_loss": round(val - invested, 2)
        })

    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "total_gain_loss": round(current_value - total_invested, 2),
        "holdings": holdings
    }

# --- EXPENSES ENDPOINTS ---
@router.post("/expenses/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/expenses/", response_model=List[ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()
