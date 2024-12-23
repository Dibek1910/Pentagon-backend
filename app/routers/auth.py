from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, constr
from app.services.otp_service import generate_otp, store_otp, validate_stored_otp

router = APIRouter(prefix="/auth", tags=["Authentication"])

class OTPRequest(BaseModel):
    mobile_number: constr(regex="^[0-9]{10}$")

class OTPValidationRequest(BaseModel):
    mobile_number: constr(regex="^[0-9]{10}$")
    otp: constr(regex="^[0-9]{4}$")

@router.post("/generate-otp/")
def generate_otp_for_auth(request: OTPRequest):
    try:
        otp = generate_otp()
        store_otp(request.mobile_number, otp)
        # Here you would typically send the OTP via SMS
        print(f"Generated OTP for {request.mobile_number}: {otp}")
        return {
            "message": "OTP sent successfully",
            "success": True,
            "token": None,
            "user": {}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate-otp/")
def validate_otp(request: OTPValidationRequest):
    if validate_stored_otp(request.mobile_number, request.otp):
        return {
            "message": "OTP validated successfully",
            "success": True,
            "token": "dummy_token",  # In production, generate a real JWT token
            "user": {"mobile_number": request.mobile_number}
        }
    raise HTTPException(status_code=400, detail="Invalid OTP")

