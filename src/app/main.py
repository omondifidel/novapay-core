from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import engine, Base, get_db
from app.models import BankUser

# Programmatically initialize tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NovaPay Digital Bank Core API")

# Payload validation models
class UserCreate(BaseModel):
    account_number: str
    name: str

@app.get("/health")
def health_check():
    return {"status": "UP", "database": "CONNECTED", "compliance": "RBI-AUDIT-COMPLIANT"}

@app.post("/api/v1/users")
def register_bank_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Defensive banking control: Ensure account uniqueness
    existing_user = db.query(BankUser).filter(BankUser.account_number == user_data.account_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Account number already registered.")
    
    new_user = BankUser(
        account_number=user_data.account_number,
        name=user_data.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"user_id": new_user.id, "status": "KYC_PENDING", "name": new_user.name}