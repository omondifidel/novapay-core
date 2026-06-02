from sqlalchemy import Column, Integer, String
from app.database import Base

class BankUser(Base):
    """
    NovaPay Core User Database Table Entity Schema.
    Tracks structural account records mapped to KYC details.
    """
    __tablename__ = "bank_users"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    
    # ─── LEGACY BASELINE COLUMN ──────────────────────────────────────────
    # This represents our initial Phase 0 database design state.
    # We will later split this into first_name and last_name with zero downtime!
    name = Column(String, nullable=False)