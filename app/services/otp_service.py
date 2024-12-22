import random
from datetime import datetime, timedelta

otp_store = {}  # In-memory store. In production, use a proper database or cache

def generate_otp():
    return str(random.randint(1000, 9999))

def store_otp(mobile_number: str, otp: str):
    expiry = datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
    otp_store[mobile_number] = {"otp": otp, "expiry": expiry}

def validate_stored_otp(mobile_number: str, otp: str) -> bool:
    stored = otp_store.get(mobile_number)
    if not stored:
        return False
    if datetime.now() > stored["expiry"]:
        del otp_store[mobile_number]
        return False
    if otp == stored["otp"]:
        del otp_store[mobile_number]
        return True
    return False
