from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer, Account
from app.schemas import CustomerCreate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    # Create a default account for the customer
    default_account = Account(customer_id=db_customer.id, account_type="Savings")
    db.add(default_account)
    db.commit()
    db.refresh(default_account)

    # Update the customer with the primary account
    db_customer.primary_account_id = default_account.id
    db.commit()
    db.refresh(db_customer)

    return db_customer

