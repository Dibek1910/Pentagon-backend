import random
from datetime import datetime, timedelta

# In-memory store for OTPs. In production, use Redis or a database
otp_store = {}

def generate_otp() -> str:
    """Generate a 4-digit OTP."""
    return str(random.randint(1000, 9999))

def store_otp(mobile_number: str, otp: str) -> None:
    """Store OTP with 5-minute expiry."""
    expiry = datetime.now() + timedelta(minutes=5)
    otp_store[mobile_number] = {
        "otp": otp,
        "expiry": expiry
    }
    print(f"Stored OTP for {mobile_number}: {otp} (expires at {expiry})")

def validate_stored_otp(mobile_number: str, otp: str) -> bool:
    """Validate the OTP for the given mobile number."""
    stored = otp_store.get(mobile_number)
    if not stored:
        print(f"No OTP found for {mobile_number}")
        return False
    
    if datetime.now() > stored["expiry"]:
        print(f"OTP expired for {mobile_number}")
        del otp_store[mobile_number]
        return False
    
    if otp == stored["otp"]:
        print(f"OTP validated successfully for {mobile_number}")
        del otp_store[mobile_number]
        return True
    
    print(f"Invalid OTP for {mobile_number}")
    return False
