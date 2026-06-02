import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Financial applications pull connection secrets from secure system environments
# We default to an in-memory SQLite engine for localized unit testing isolation
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# The Engine provides the actual core binary communication link to the database server
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# SessionLocal instances represent an active database transaction workspace session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DeclarativeBase is the target foundation registry that tracks all our database table structures
Base = declarative_base()

def get_db():
    """
    Dependency Provider Pattern.
    Yields an active transaction session to a web request, and guarantees 
    the connection safely closes after the API request finishes processing.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()