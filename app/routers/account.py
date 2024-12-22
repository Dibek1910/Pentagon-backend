from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account
from app.schemas import AccountBase, AccountResponse

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountBase, customer_id: int, db: Session = Depends(get_db)):
    db_account = Account(**account.dict(), customer_id=customer_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
