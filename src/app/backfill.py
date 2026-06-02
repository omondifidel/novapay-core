import sys
import os

# Align python path lookup context if script is executed standalone
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.app.database import SessionLocal
from src.app.models import BankUser

def run_backfill():
    """
    Administrative Migration Utility.
    Finds historical Phase 0 records missing segmented names and 
    retroactively populates them without taking the application offline.
    """
    db = SessionLocal()
    try:
        print("🚀 Initiating NovaPay Core Database Backfill Processing...")
        
        # Scan for users where new columns exist as null, but legacy data is populated
        legacy_users = db.query(BankUser).filter(
            BankUser.name.isnot(None),
            (BankUser.first_name.is_(None)) | (BankUser.last_name.is_(None))
        ).all()
        
        print(f"🔍 Found {len(legacy_users)} historical rows requiring structural backfilling.")
        
        mutated_count = 0
        for user in legacy_users:
            name_parts = user.name.strip().split(" ", 1)
            user.first_name = name_parts[0] if name_parts else "Unknown"
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""
            mutated_count += 1
            
        db.commit()
        print(f"✅ Structural Backfill complete! Successfully migrated {mutated_count} account records.")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Critical error during backfill processing: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    run_backfill()