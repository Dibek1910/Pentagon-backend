from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    phone_number: str
    email: EmailStr
    gender: str
    dob: date
    current_address: str
    current_city: str
    current_state: str
    current_pincode: str
    is_permanent_same_as_current: bool
    permanent_address: str
    permanent_city: str
    permanent_state: str
    permanent_pincode: str

class CustomerCreate(CustomerBase):
    password: str

class CustomerResponse(CustomerBase):
    id: int
    primary_account_id: Optional[int] = None

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    account_type: str
    currency: str = "INR"
    balance: float = 0.0

class AccountCreate(AccountBase):
    customer_id: int

class AccountResponse(AccountBase):
    id: int
    customer_id: int
    status: str

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    document_type: str
    document_path: str

class DocumentCreate(DocumentBase):
    customer_id: int

class DocumentResponse(DocumentBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True

class OTPRequest(BaseModel):
    mobile_number: str = Field(..., pattern="^[0-9]{10}$")

class OTPValidationRequest(BaseModel):
    mobile_number: str = Field(..., pattern="^[0-9]{10}$")
    otp: str = Field(..., pattern="^[0-9]{4}$")

class SignInRequest(BaseModel):
    user_id: str
    password: str

