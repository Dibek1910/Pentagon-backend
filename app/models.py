from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    address = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    dob = Column(Date, nullable=False)
    password = Column(String, nullable=False)
    primary_account_id = Column(Integer, ForeignKey("accounts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    accounts = relationship("Account", back_populates="customer", foreign_keys="Account.customer_id")
    primary_account = relationship("Account", foreign_keys=[primary_account_id])

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="USD")
    status = Column(String, default="Active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="accounts", foreign_keys=[customer_id])

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    document_type = Column(String, nullable=False)
    document_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
