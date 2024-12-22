from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, customer, account, notification, document

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:4200",
    "https://your-production-frontend-domain.com",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(account.router)
app.include_router(notification.router)
app.include_router(document.router)

@app.get("/")
def root():
    return {"message": "Welcome to ABC Bank API"}
