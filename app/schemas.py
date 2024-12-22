from pydantic import BaseModel
from typing import Optional
from datetime import date

class AuthResponse(BaseModel):
    message: str
    success: bool = True
    token: str | None = None
    user: dict | None = None

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: Optional[str] = None
    address: str
    gender: Optional[str] = None
    dob: date

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    primary_account_id: Optional[int] = None

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    account_type: str
    currency: Optional[str] = "USD"
    balance: Optional[float] = 0.0

class AccountResponse(AccountBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True

class DocumentBase(BaseModel):
    document_type: str
    document_path: str
