from fastapi import APIRouter
from app.services.notification_service import send_sms

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/send/")
def send_notification(mobile_number: str, message: str):
    response = send_sms(mobile_number, message)
    return {"status": "Success", "response": response}