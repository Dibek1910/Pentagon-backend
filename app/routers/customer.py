from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Customer, Account
from app.schemas import CustomerCreate, CustomerResponse
from app.services.auth_service import hash_password

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(customer.password)
    db_customer = Customer(**customer.dict(exclude={"password"}), password=hashed_password)
    
    try:
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

    except IntegrityError as e:
        db.rollback()
        error_info = str(e.orig)
        if "phone_number" in error_info:
            raise HTTPException(status_code=400, detail="Phone number already registered")
        elif "email" in error_info:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="An error occurred while creating the customer")

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer