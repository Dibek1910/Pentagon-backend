from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.orm import Session 
from app.database import get_db 
from app.schemas import OTPRequest, OTPValidationRequest, SignInRequest 
from app.services.otp_service import generate_otp, store_otp, validate_stored_otp 
from app.models import Customer 
from passlib.context import CryptContext 
 
router = APIRouter(prefix="/auth", tags=["Authentication"]) 
 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
 
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
 
@router.post("/signin/") 
def sign_in(request: SignInRequest, db: Session = Depends(get_db)): 
    customer = db.query(Customer).filter(Customer.id == request.user_id).first() 
    if not customer or not pwd_context.verify(request.password, customer.password): 
        raise HTTPException(status_code=400, detail="Invalid credentials") 
    return { 
        "message": "Sign in successful", 
        "success": True, 
        "token": "dummy_token",  # In production, generate a real JWT token 
        "user": {"id": customer.id, "email": customer.email} 
    }

