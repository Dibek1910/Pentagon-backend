import re
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer, Account
from app.schemas import CustomerCreate, CustomerResponse
from passlib.context import CryptContext

router = APIRouter(prefix="/customers", tags=["Customers"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def is_valid_email(email: str) -> bool:
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email) is not None

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    if not is_valid_email(customer.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Generate a unique 11-digit customer ID
    while True:
        customer_id = random.randint(10000000000, 99999999999)
        if not db.query(Customer).filter(Customer.id == customer_id).first():
            break
    
    hashed_password = pwd_context.hash(customer.password)
    db_customer = Customer(id=customer_id, **customer.dict(exclude={"password"}), password=hashed_password)
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

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

