from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Date, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    current_address = Column(String, nullable=False)
    current_city = Column(String, nullable=False)
    current_state = Column(String, nullable=False)
    current_pincode = Column(String, nullable=False)
    is_permanent_same_as_current = Column(Boolean, default=False)
    permanent_address = Column(String, nullable=False)
    permanent_city = Column(String, nullable=False)
    permanent_state = Column(String, nullable=False)
    permanent_pincode = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_kyc_verified = Column(Boolean, default=False)
    primary_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    accounts = relationship(
        "Account",
        back_populates="customer",
        foreign_keys="[Account.customer_id]",
        primaryjoin="Customer.id==Account.customer_id"
    )
    primary_account = relationship(
        "Account",
        foreign_keys=[primary_account_id],
        post_update=True
    )

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="INR")
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    customer = relationship(
        "Customer",
        back_populates="accounts",
        foreign_keys=[customer_id]
    )

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(BigInteger, ForeignKey("customers.id"), nullable=False)
    document_type = Column(String, nullable=False)
    document_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    customer = relationship("Customer")

