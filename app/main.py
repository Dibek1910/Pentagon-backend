from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, customer, account, notification, document
import os

app = FastAPI(title="ABC Bank API", version="1.0.0")

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

