"""
Mock Banking API Server
Provides REST API endpoints for banking operations
Run with: uvicorn mock_banking_api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="VaaniPay Mock Banking API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database
USERS = {
    "rahul_sharma": {
        "user_id": "USER001",
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "accounts": [
            {
                "account_number": "4421",
                "account_type": "Primary Savings",
                "balance": 27940.0,
                "currency": "INR"
            },
            {
                "account_number": "9920",
                "account_type": "Salary Account",
                "balance": 3210.0,
                "currency": "INR"
            },
            {
                "account_number": "1187",
                "account_type": "Fixed Deposit",
                "balance": 112785.0,
                "currency": "INR"
            }
        ],
        "contacts": [
            {
                "name": "Anjali Verma",
                "phone": "9876543210",
                "account": "ACC_ANJALI"
            },
            {
                "name": "Ramesh Kumar",
                "phone": "9123456789",
                "account": "ACC_RAMESH"
            },
            {
                "name": "Father",
                "phone": "9988776655",
                "account": "ACC_FATHER"
            }
        ],
        "bills": [
            {
                "biller": "BESCOM",
                "amount": 720.0,
                "due_date": "2025-11-30",
                "status": "pending"
            },
            {
                "biller": "Water",
                "amount": 350.0,
                "due_date": "2025-11-28",
                "status": "pending"
            },
            {
                "biller": "Gas",
                "amount": 845.0,
                "due_date": "2025-12-05",
                "status": "pending"
            }
        ],
        "transactions": [
            {
                "id": "TXN001",
                "amount": -750.0,
                "type": "transfer",
                "description": "to Anjali Verma",
                "timestamp": "2025-11-22T17:30:00",
                "category": "transfer"
            },
            {
                "id": "TXN002",
                "amount": -1200.0,
                "type": "bill_payment",
                "description": "BESCOM bill payment",
                "timestamp": "2025-11-21T14:15:00",
                "category": "utilities"
            },
            {
                "id": "TXN003",
                "amount": 5000.0,
                "type": "credit",
                "description": "Salary credit",
                "timestamp": "2025-11-20T09:00:00",
                "category": "income"
            },
            {
                "id": "TXN004",
                "amount": -399.0,
                "type": "payment",
                "description": "Airtel mobile recharge",
                "timestamp": "2025-11-19T18:45:00",
                "category": "mobile"
            },
            {
                "id": "TXN005",
                "amount": -2200.0,
                "type": "transfer",
                "description": "transfer to Father",
                "timestamp": "2025-11-18T11:30:00",
                "category": "transfer"
            },
            {
                "id": "TXN006",
                "amount": -850.0,
                "type": "payment",
                "description": "grocery shopping at BigBazaar",
                "timestamp": "2025-11-17T16:20:00",
                "category": "groceries"
            },
            {
                "id": "TXN007",
                "amount": 500.0,
                "type": "credit",
                "description": "Amazon refund",
                "timestamp": "2025-11-16T13:10:00",
                "category": "refund"
            },
            {
                "id": "TXN008",
                "amount": -450.0,
                "type": "payment",
                "description": "restaurant payment",
                "timestamp": "2025-11-15T20:30:00",
                "category": "dining"
            },
            {
                "id": "TXN009",
                "amount": -1100.0,
                "type": "bill_payment",
                "description": "utility bills",
                "timestamp": "2025-11-14T10:00:00",
                "category": "utilities"
            },
            {
                "id": "TXN010",
                "amount": -300.0,
                "type": "payment",
                "description": "movie tickets booking",
                "timestamp": "2025-11-13T19:15:00",
                "category": "entertainment"
            }
        ],
        "credit_limit": 250000.0,
        "credit_utilized": 0.0
    },
    "priya_patel": {
        "user_id": "USER002",
        "name": "Priya Patel",
        "phone": "9845612378",
        "accounts": [
            {
                "account_number": "5532",
                "account_type": "Savings Account",
                "balance": 45600.0,
                "currency": "INR"
            },
            {
                "account_number": "7789",
                "account_type": "Current Account",
                "balance": 15240.0,
                "currency": "INR"
            }
        ],
        "contacts": [
            {
                "name": "Amit Shah",
                "phone": "9876501234",
                "account": "ACC_AMIT"
            },
            {
                "name": "Mother",
                "phone": "9823456789",
                "account": "ACC_MOTHER"
            }
        ],
        "bills": [
            {
                "biller": "Airtel",
                "amount": 599.0,
                "due_date": "2025-11-25",
                "status": "pending"
            },
            {
                "biller": "Internet",
                "amount": 899.0,
                "due_date": "2025-11-28",
                "status": "pending"
            }
        ],
        "transactions": [
            {
                "id": "TXN201",
                "amount": -599.0,
                "type": "payment",
                "description": "Airtel postpaid",
                "timestamp": "2025-11-21T10:30:00",
                "category": "mobile"
            },
            {
                "id": "TXN202",
                "amount": 8000.0,
                "type": "credit",
                "description": "Freelance payment",
                "timestamp": "2025-11-20T15:45:00",
                "category": "income"
            },
            {
                "id": "TXN203",
                "amount": -1200.0,
                "type": "transfer",
                "description": "to Mother",
                "timestamp": "2025-11-19T12:00:00",
                "category": "transfer"
            }
        ],
        "credit_limit": 150000.0,
        "credit_utilized": 0.0
    },
    "arjun_reddy": {
        "user_id": "USER003",
        "name": "Arjun Reddy",
        "phone": "9912345678",
        "accounts": [
            {
                "account_number": "3366",
                "account_type": "Premium Savings",
                "balance": 185000.0,
                "currency": "INR"
            },
            {
                "account_number": "8844",
                "account_type": "Investment Account",
                "balance": 550000.0,
                "currency": "INR"
            }
        ],
        "contacts": [
            {
                "name": "Sneha Rao",
                "phone": "9876012345",
                "account": "ACC_SNEHA"
            },
            {
                "name": "Brother",
                "phone": "9845678901",
                "account": "ACC_BROTHER"
            },
            {
                "name": "Business Partner",
                "phone": "9823344556",
                "account": "ACC_PARTNER"
            }
        ],
        "bills": [
            {
                "biller": "Credit Card",
                "amount": 12500.0,
                "due_date": "2025-11-30",
                "status": "pending"
            },
            {
                "biller": "Electricity",
                "amount": 2350.0,
                "due_date": "2025-12-02",
                "status": "pending"
            }
        ],
        "transactions": [
            {
                "id": "TXN301",
                "amount": -12500.0,
                "type": "payment",
                "description": "Credit card payment",
                "timestamp": "2025-11-22T09:15:00",
                "category": "payment"
            },
            {
                "id": "TXN302",
                "amount": 50000.0,
                "type": "credit",
                "description": "Business income",
                "timestamp": "2025-11-20T11:30:00",
                "category": "income"
            },
            {
                "id": "TXN303",
                "amount": -25000.0,
                "type": "transfer",
                "description": "to Business Partner",
                "timestamp": "2025-11-18T14:20:00",
                "category": "business"
            }
        ],
        "credit_limit": 500000.0,
        "credit_utilized": 0.0
    },
    "ananya_krishnan": {
        "user_id": "USER004",
        "name": "Ananya Krishnan",
        "phone": "9745678901",
        "accounts": [
            {
                "account_number": "2211",
                "account_type": "Student Account",
                "balance": 8500.0,
                "currency": "INR"
            }
        ],
        "contacts": [
            {
                "name": "Roommate",
                "phone": "9876543210",
                "account": "ACC_ROOMMATE"
            },
            {
                "name": "Dad",
                "phone": "9823456780",
                "account": "ACC_DAD"
            }
        ],
        "bills": [
            {
                "biller": "Netflix",
                "amount": 199.0,
                "due_date": "2025-11-26",
                "status": "pending"
            },
            {
                "biller": "Spotify",
                "amount": 119.0,
                "due_date": "2025-11-28",
                "status": "pending"
            }
        ],
        "transactions": [
            {
                "id": "TXN401",
                "amount": 5000.0,
                "type": "credit",
                "description": "Scholarship",
                "timestamp": "2025-11-20T10:00:00",
                "category": "income"
            },
            {
                "id": "TXN402",
                "amount": -650.0,
                "type": "payment",
                "description": "Books purchase",
                "timestamp": "2025-11-19T16:30:00",
                "category": "education"
            },
            {
                "id": "TXN403",
                "amount": -1200.0,
                "type": "transfer",
                "description": "to Roommate - rent split",
                "timestamp": "2025-11-18T20:00:00",
                "category": "transfer"
            }
        ],
        "credit_limit": 50000.0,
        "credit_utilized": 0.0
    }
}

LOAN_PRODUCTS = [
    {
        "type": "Personal Loan",
        "interest_rate": 10.5,
        "max_amount": 500000,
        "min_tenure": 1,
        "max_tenure": 5,
        "unit": "years"
    },
    {
        "type": "Home Loan",
        "interest_rate": 8.5,
        "max_amount": 5000000,
        "min_tenure": 1,
        "max_tenure": 20,
        "unit": "years"
    },
    {
        "type": "Car Loan",
        "interest_rate": 9.2,
        "max_amount": 1500000,
        "min_tenure": 1,
        "max_tenure": 7,
        "unit": "years"
    },
    {
        "type": "Education Loan",
        "interest_rate": 9.0,
        "max_amount": 2000000,
        "min_tenure": 1,
        "max_tenure": 10,
        "unit": "years"
    }
]

INTEREST_RATES = {
    "savings_account": 3.5,
    "fd_1_year": 6.8,
    "fd_3_years": 7.2,
    "recurring_deposit": 6.5
}

# Pydantic Models
class Account(BaseModel):
    account_number: str
    account_type: str
    balance: float
    currency: str = "INR"

class Transaction(BaseModel):
    id: str
    amount: float
    type: str
    description: str
    timestamp: str
    category: str

class TransferRequest(BaseModel):
    from_account: str
    to_contact: str
    amount: float
    pin: str

class BillPaymentRequest(BaseModel):
    account: str
    biller: str
    amount: float
    pin: str

# API Endpoints

@app.get("/")
def root():
    return {
        "service": "VaaniPay Mock Banking API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/users/{user_id}/accounts")
def get_accounts(user_id: str = "rahul_sharma"):
    """Get all accounts for a user"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return {"accounts": USERS[user_id]["accounts"]}

@app.get("/api/accounts/{account_number}/user")
def get_user_by_account(account_number: str):
    """Find user_id by account number"""
    for user_id, user_data in USERS.items():
        for account in user_data["accounts"]:
            if account["account_number"] == account_number:
                return {
                    "user_id": user_id,
                    "name": user_data["name"],
                    "account_number": account_number,
                    "account_type": account["account_type"]
                }
    raise HTTPException(status_code=404, detail="Account not found")

@app.get("/api/accounts/{account_number}/balance")
def get_balance(account_number: str, user_id: str = None):
    """Get balance for a specific account"""
    # If user_id not provided, find it by account number
    if user_id is None:
        for uid, user_data in USERS.items():
            for account in user_data["accounts"]:
                if account["account_number"] == account_number:
                    user_id = uid
                    break
            if user_id:
                break
        if user_id is None:
            raise HTTPException(status_code=404, detail="Account not found")
    
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    for account in USERS[user_id]["accounts"]:
        if account["account_number"] == account_number:
            return {
                "account_number": account_number,
                "balance": account["balance"],
                "currency": account["currency"],
                "account_type": account["account_type"]
            }
    
    raise HTTPException(status_code=404, detail="Account not found")

@app.get("/api/users/{user_id}/transactions")
def get_transactions(user_id: str = "rahul_sharma", limit: int = 10):
    """Get recent transactions"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = USERS[user_id]["transactions"][:limit]
    return {"transactions": transactions, "count": len(transactions)}

@app.get("/api/users/{user_id}/bills")
def get_bills(user_id: str = "rahul_sharma"):
    """Get pending bills"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"bills": USERS[user_id]["bills"]}

@app.get("/api/users/{user_id}/contacts")
def get_contacts(user_id: str = "rahul_sharma"):
    """Get saved contacts"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"contacts": USERS[user_id]["contacts"]}

@app.get("/api/loans")
def get_loan_products():
    """Get available loan products"""
    return {"loan_products": LOAN_PRODUCTS}

@app.get("/api/users/{user_id}/credit-limit")
def get_credit_limit(user_id: str = "rahul_sharma"):
    """Get credit limit information"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = USERS[user_id]
    return {
        "credit_limit": user["credit_limit"],
        "credit_utilized": user["credit_utilized"],
        "credit_available": user["credit_limit"] - user["credit_utilized"]
    }

@app.get("/api/interest-rates")
def get_interest_rates():
    """Get current interest rates"""
    return {"interest_rates": INTEREST_RATES}

@app.post("/api/transfer")
def transfer_money(request: TransferRequest):
    """Execute money transfer (mock)"""
    # Mock PIN validation
    if request.pin != "1234":
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    return {
        "status": "success",
        "transaction_id": f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": f"Successfully transferred ₹{request.amount} to {request.to_contact}",
        "from_account": request.from_account,
        "amount": request.amount,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/pay-bill")
def pay_bill(request: BillPaymentRequest):
    """Pay bill (mock)"""
    # Mock PIN validation
    if request.pin != "1234":
        raise HTTPException(status_code=401, detail="Invalid PIN")
    
    return {
        "status": "success",
        "transaction_id": f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "message": f"Successfully paid ₹{request.amount} to {request.biller}",
        "biller": request.biller,
        "amount": request.amount,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/users/{user_id}/loan-eligibility")
def check_loan_eligibility(user_id: str = "rahul_sharma", loan_type: str = "Personal Loan"):
    """Check loan eligibility"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Mock eligibility logic
    return {
        "eligible": True,
        "loan_type": loan_type,
        "max_eligible_amount": 300000,
        "pre_approved": True,
        "message": f"You are pre-approved for {loan_type} up to ₹3,00,000"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting VaaniPay Mock Banking API on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

