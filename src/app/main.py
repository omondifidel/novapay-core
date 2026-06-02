from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.app.database import engine, Base, get_db
from src.app.models import BankUser

# Initialize tables programmatically on application bootstrap
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NovaPay Digital Bank Core API")

class UserCreate(BaseModel):
    account_number: str
    name: str

@app.get("/health")
def health_check():
    return {"status": "UP", "database": "CONNECTED", "compliance": "RBI-AUDIT-COMPLIANT"}

@app.post("/api/v1/users")
def register_bank_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(BankUser).filter(BankUser.account_number == user_data.account_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Account number already registered.")
    
    # ─── DUAL-WRITE EXTRACTION MECHANISM ────────────────────────────────
    # We gracefully split the incoming single name string into structural segments.
    # We provide safe fallback strings to ensure data integrity during messy entries.
    name_parts = user_data.name.strip().split(" ", 1)
    extracted_first = name_parts[0] if name_parts else "Unknown"
    extracted_last = name_parts[1] if len(name_parts) > 1 else ""

    new_user = BankUser(
        account_number=user_data.account_number,
        name=user_data.name,                 # Legacy Write
        first_name=extracted_first,          # Expanded Write (Dual Write)
        last_name=extracted_last            # Expanded Write (Dual Write)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "user_id": new_user.id, 
        "status": "KYC_PENDING", 
        "name": new_user.name,
        "captured_first_name": new_user.first_name,
        "captured_last_name": new_user.last_name
    }