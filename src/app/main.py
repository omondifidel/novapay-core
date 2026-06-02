from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.app.database import engine, Base, get_db
from src.app.models import BankUser

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NovaPay Digital Bank Core API")

# 1. Ensure the Pydantic schema expects ONLY the split names
class UserCreate(BaseModel):
    account_number: str
    first_name: str
    last_name: str

@app.get("/health")
def health_check():
    return {"status": "UP", "database": "CONNECTED", "compliance": "RBI-AUDIT-COMPLIANT"}

@app.post("/api/v1/users")
def register_bank_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(BankUser).filter(BankUser.account_number == user_data.account_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Account number already registered.")
    
    # 2. Absolute clean instantiation. Ensure 'name=' is NOT here!
    new_user = BankUser(
        account_number=user_data.account_number,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "user_id": new_user.id, 
        "status": "KYC_PENDING", 
        "captured_first_name": new_user.first_name,
        "captured_last_name": new_user.last_name
    }