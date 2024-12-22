from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging
from typing import Optional
from app.database import SessionLocal, engine
from app.models import Base, User
from sqlalchemy.orm import Session
from app.services.otp_service import validate_stored_otp

logger = logging.getLogger(__name__)

router = APIRouter()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

class OTPRequest(BaseModel):
    mobile_number: str

@router.get("/")
async def root():
    return {"message": "Hello World"}

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-otp/")
async def send_otp(request: OTPRequest, db: Session = Depends(get_db)):
    logger.info(f"Sending OTP to mobile number: {request.mobile_number}")
    # Add your OTP sending logic here
    return {"message": "OTP sent successfully"}

@router.post("/validate-otp/")
def validate_otp(request: OTPRequest, otp: str):
    logger.info(f"Validating OTP for mobile number: {request.mobile_number}")
    if validate_stored_otp(request.mobile_number, otp):
        logger.info("OTP validated successfully")
        return {"message": "OTP validated successfully"}
    logger.error("Invalid OTP")
    raise HTTPException(status_code=400, detail="Invalid OTP")

@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@router.get("/users/me")
async def read_users_me(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/users/")
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user