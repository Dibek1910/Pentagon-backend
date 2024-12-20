from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from app.schemas import CustomerResponse
from app.services.auth_service import verify_password
from app.services.otp_service import generate_otp, store_otp, validate_stored_otp
from pydantic import BaseModel
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

class OTPRequest(BaseModel):
    mobile_number: str

@router.post("/generate-otp/")
def generate_otp_for_auth(request: OTPRequest):
    mobile_number = request.mobile_number
    if len(mobile_number) != 10 or not mobile_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid mobile number")
    otp = generate_otp()
    store_otp(mobile_number, otp)
    
    # Log the OTP (for debugging purposes only)
    logger.info(f"Generated OTP for {mobile_number}: {otp}")
    
    # Here, send OTP using notification service (placeholder)
    return {"message": "OTP sent successfully"}

@router.post("/validate-otp/")
def validate_otp(request: OTPRequest, otp: str):
    if validate_stored_otp(request.mobile_number, otp):
        return {"message": "OTP validated successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")

@router.post("/signin/", response_model=CustomerResponse)
def sign_in(account_id: int, password: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == account_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if not verify_password(password, customer.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    return customer