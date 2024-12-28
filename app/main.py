from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, customer, account, notification, document
import os
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.database import engine

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:4200",  # Angular dev server
    "https://your-production-frontend-domain.com",  # Add your production frontend URL when you have it
    "*",  # Allow all origins for now (you may want to restrict this in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Test database connection
try:
    with engine.connect() as connection:
        logger.info("Successfully connected to the database")
except SQLAlchemyError as e:
    logger.error(f"Error connecting to the database: {str(e)}")

app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(account.router)
app.include_router(notification.router)
app.include_router(document.router)

@app.get("/")
def root():
    return {"message": "Welcome to ABC Bank API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)

