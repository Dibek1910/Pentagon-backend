from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class CustomerBase(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    phone_number: str
    email: str
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

    model_config = ConfigDict(from_attributes=True)

class AccountBase(BaseModel):
    account_type: str
    currency: Optional[str] = "USD"
    balance: Optional[float] = 0.0

class AccountResponse(AccountBase):
    id: int
    customer_id: int

    model_config = ConfigDict(from_attributes=True)

class DocumentBase(BaseModel):
    document_type: str
    document_path: str

