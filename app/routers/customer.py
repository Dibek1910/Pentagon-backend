from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    gender = Column(String)
    dob = Column(Date)
    current_address = Column(String)
    current_city = Column(String)
    current_state = Column(String)
    current_pincode = Column(String)
    is_permanent_same_as_current = Column(Boolean, default=False)
    permanent_address = Column(String)
    permanent_city = Column(String)
    permanent_state = Column(String)
    permanent_pincode = Column(String)
    password = Column(String)

    # Explicitly define the relationship with Account
    accounts = relationship("Account", back_populates="customer", foreign_keys="Account.customer_id")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    account_type = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    # Define the back-reference to Customer
    customer = relationship("Customer", back_populates="accounts")

