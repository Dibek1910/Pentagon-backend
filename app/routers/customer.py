import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import exc as SQLAlchemyError
from app.database import get_db
from app.models import Customer, Account
from app.schemas import CustomerCreate, CustomerResponse
from passlib.context import CryptContext
import logging
from app.auth import get_current_user_id  # Assuming you have this function in your auth module

router = APIRouter(prefix="/customers", tags=["Customers"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email) is not None

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    if not is_valid_email(customer.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    try:
        hashed_password = pwd_context.hash(customer.password)
        db_customer = Customer(**customer.dict(exclude={"password"}), password=hashed_password)
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
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the customer")

@router.get("/account-details", response_model=CustomerResponse)
def get_account_details(db: Session = Depends(get_db)):
    current_user_id = get_current_user_id()
    customer = db.query(Customer).filter(Customer.id == current_user_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

