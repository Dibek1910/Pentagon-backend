from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from app.schemas import AuthResponse
from app.services.otp_service import generate_otp, store_otp, validate_stored_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/generate-otp/")
def generate_otp_for_auth(mobile_number: str) -> AuthResponse:
    if len(mobile_number) != 10 or not mobile_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid mobile number")
    otp = generate_otp()
    store_otp(mobile_number, otp)
    # Here, send OTP using notification service (placeholder)
    return AuthResponse(message="OTP sent successfully")

@router.post("/validate-otp/")
def validate_otp(mobile_number: str, otp: str) -> AuthResponse:
    if validate_stored_otp(mobile_number, otp):
        return AuthResponse(message="OTP validated successfully")
    raise HTTPException(status_code=400, detail="Invalid OTP")

@router.post("/signin/")
def sign_in(account_id: str, password: str, db: Session = Depends(get_db)) -> AuthResponse:
    customer = db.query(Customer).filter(Customer.id == account_id).first()
    if not customer or customer.password != password:  # In production, use proper password hashing
        raise HTTPException(status_code=401, detail="Invalid account ID or password")
    return AuthResponse(message="Sign in successful", token="dummy_token", user={"id": customer.id})

