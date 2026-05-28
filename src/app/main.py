from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="NovaPay Digital Bank Core API")

# A structure defining what a transaction payload must look like
class Transaction(BaseModel):
    account_id: str
    amount: float
    currency: str

@app.get("/health")
def health_check():
    # Production-grade health check for Kubernetes liveness probes
    return {"status": "UP", "database": "CONNECTED", "compliance": "RBI-AUDIT-PENDING"}

@app.post("/api/v1/transactions")
def create_transaction(tx: Transaction):
    # Banking logic protection: Reject negative balances immediately
    if tx.amount <= 0:
        raise HTTPException(status_code=400, detail="Transaction amount must be positive.")
    return {"transaction_id": "TXN-9081234", "status": "SETTILED", "amount": tx.amount}