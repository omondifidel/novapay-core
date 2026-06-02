from sqlalchemy import Column, Integer, String
from src.app.database import Base

class BankUser(Base):
    """
    NovaPay Core User Database Table Entity Schema.
    Tracks structural account records mapped to KYC details.
    """
    __tablename__ = "bank_users"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    
    # ─── LEGACY PHASE 0 COLUMN ──────────────────────────────────────────
    # Kept fully alive so legacy microservices don't break on execution
    name = Column(String, nullable=False)
    
    # ─── PHASE 1: EXPANDED CO-EXISTENCE COLUMNS ──────────────────────────
    # These must remain nullable=True initially because legacy database rows 
    # from Phase 0 do not contain separate first/last name values yet!
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)