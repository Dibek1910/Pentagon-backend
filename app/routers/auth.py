from fastapi import APIRouter, HTTPException
from app.services.otp_service import generate_otp, store_otp, validate_stored_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/generate-otp/")
def generate_otp_for_auth(mobile_number: str):
    if len(mobile_number) != 10 or not mobile_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid mobile number")
    otp = generate_otp()
    store_otp(mobile_number, otp)
    # Here, send OTP using notification service (placeholder)
    return {"message": "OTP sent successfully"}

@router.post("/validate-otp/")
def validate_otp(mobile_number: str, otp: str):
    if validate_stored_otp(mobile_number, otp):
        return {"message": "OTP validated successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")

