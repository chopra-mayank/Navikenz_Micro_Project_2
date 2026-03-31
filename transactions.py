from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from sqlalchemy import func
from datetime import datetime
import calendar

router = APIRouter()

@router.post("/transactions")
def add_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
    new_txn = models.Transaction(
        amount=txn.amount,
        type=txn.type,
        user_id=txn.user_id,
        category_id=txn.category_id
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    
    # Check budget for expense alerts
    if txn.type == "expense":
        budget = db.query(models.Budget).filter(
            models.Budget.user_id == txn.user_id,
            models.Budget.category_id == txn.category_id
        ).first()
        if budget:
            total_expense = db.query(func.sum(models.Transaction.amount)).filter(
                models.Transaction.user_id == txn.user_id,
                models.Transaction.category_id == txn.category_id,
                models.Transaction.type == "expense"
            ).scalar() or 0
            
            if total_expense > budget.limit:
                alert = models.Alert(
                    message=f"Budget exceeded for category {txn.category_id}. Total expense: {total_expense}, Limit: {budget.limit}",
                    user_id=txn.user_id
                )
                db.add(alert)
                db.commit()

    return {"message": "Transaction added successfully", "transaction_id": new_txn.id}

@router.get("/transactions")
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

@router.post("/budgets")
def add_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    new_budget = models.Budget(
        limit=budget.limit,
        user_id=budget.user_id,
        category_id=budget.category_id
    )
    db.add(new_budget)
    db.commit()
    return {"message": "Budget created"}

@router.get("/budgets")
def get_budgets(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()

@router.get("/reports/monthly")
def get_monthly_report(user_id: int, month: int = None, year: int = None, db: Session = Depends(get_db)):
    if not month or not year:
        now = datetime.utcnow()
        month = month or now.month
        year = year or now.year

    start_date = datetime(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day, 23, 59, 59, 999999)

    income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == "income",
        models.Transaction.date >= start_date,
        models.Transaction.date <= end_date
    ).scalar() or 0
    expense = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == "expense",
        models.Transaction.date >= start_date,
        models.Transaction.date <= end_date
    ).scalar() or 0
    
    return {
        "user_id": user_id,
        "month": month,
        "year": year,
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense
    }

@router.get("/alerts")
def get_alerts(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.user_id == user_id).all()
