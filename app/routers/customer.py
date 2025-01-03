import random
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Customer, Account
from app.schemas import CustomerCreate, CustomerResponse
from app.services.email_service import send_personal_details_confirmation, send_account_creation_confirmation
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter(prefix="/customers", tags=["Customers"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_customer_attempt(customer_data: dict):
    sanitized_data = {k: v for k, v in customer_data.items() if k != 'password'}
    logger.info(f"Attempting to create customer with data: {sanitized_data}")

def verify_database_schema(db: Session):
    inspector = inspect(db.bind)
    tables = inspector.get_table_names()
    logger.info(f"Available tables: {tables}")
    
    required_tables = {'customers', 'accounts', 'documents'}
    if not all(table in tables for table in required_tables):
        missing = required_tables - set(tables)
        logger.error(f"Missing required tables: {missing}")
        return False
    return True

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        if not verify_database_schema(db):
            raise HTTPException(
                status_code=500,
                detail="Database schema is not properly configured"
            )

        log_customer_attempt(customer.dict())

        existing = db.query(Customer).filter(
            (Customer.phone_number == customer.phone_number) |
            (Customer.email == customer.email)
        ).first()

        if existing:
            detail = "phone number" if existing.phone_number == customer.phone_number else "email"
            logger.warning(f"Customer with this {detail} already exists")
            raise HTTPException(
                status_code=400,
                detail=f"A customer with this {detail} already exists"
            )

        customer_id = random.randint(10000000000, 99999999999)
        while db.query(Customer).filter(Customer.id == customer_id).first():
            customer_id = random.randint(10000000000, 99999999999)

        try:
            hashed_password = pwd_context.hash(customer.password)
            db_customer = Customer(
                id=customer_id,
                **customer.dict(exclude={"password"}),
                password=hashed_password,
                created_at=datetime.utcnow()
            )
            
            logger.info(f"Created customer instance with ID: {customer_id}")
            db.add(db_customer)
            db.flush()
            logger.info("Successfully flushed customer to database")

            db.commit()
            logger.info("Successfully committed transaction")
            
            db.refresh(db_customer)

            # Send email confirmation
            send_personal_details_confirmation(db_customer.email)

            return db_customer

        except Exception as e:
            logger.error(f"Error during customer creation: {str(e)}")
            db.rollback()
            raise

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail="Database integrity error. Please check your input data."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/{customer_id}/complete-kyc")
def complete_kyc_verification(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Update KYC status
    customer.is_kyc_verified = True
    
    # Generate account if not exists
    if not customer.primary_account_id:
        account = Account(
            customer_id=customer.id,
            account_type="Savings",
            balance=0.0,
            currency="INR",
            status="Active"
        )
        db.add(account)
        db.flush()
        customer.primary_account_id = account.id
    
    db.commit()
    db.refresh(customer)
    
    # Send account creation email
    send_account_creation_confirmation(
        customer.email,
        customer.id,
        customer.primary_account_id,
        "your-password"  # In production, this should be handled securely
    )
    
    return customer

@router.get("/{customer_id}/balance")
def get_account_balance(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    account = db.query(Account).filter(Account.id == customer.primary_account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account.balance

