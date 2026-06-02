import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# FIX: Switch fallback from volatile raw memory to a persistent local micro-file database 
# This preserves table structures across application and testing connection threads.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./novapay_test.db")

engine = create_engine(
    DATABASE_URL, 
    # check_same_thread=False is strictly required for SQLite to process multi-threaded API requests safely
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()