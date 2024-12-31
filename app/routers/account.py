import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account, Customer
from app.schemas import AccountCreate, AccountResponse
from app.services.notification_service import send_sms

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # Generate a unique 9-digit account ID
    while True:
        account_id = random.randint(100000000, 999999999)
        if not db.query(Account).filter(Account.id == account_id).first():
            break
    
    db_account = Account(id=account_id, **account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    # Send notification
    customer = db.query(Customer).filter(Customer.id == account.customer_id).first()
    if customer:
        message = f"Your new account has been created. Account ID: {account_id}"
        send_sms(customer.phone_number, message)
    
    return db_account

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
