# Mock Banking API Setup

## Quick Start

### 1. Install Dependencies
```bash
cd voice-agent
uv sync  # Installs FastAPI, uvicorn, httpx
```

### 2. Start Mock Banking API
```bash
# Terminal 1 - Start the Mock API
cd voice-agent
uv run python mock_banking_api.py
# Access at: http://localhost:8000
# Docs at: http://localhost:8000/docs
```

### 3. Start Voice Agent
```bash
# Terminal 2 - Start the agent
cd voice-agent
export PATH="/Users/poojareddy/.local/bin:$PATH"
uv run python src/agent.py dev
```

### 4. Start Frontend
```bash
# Terminal 3 - Start frontend
cd frontend
pnpm dev
```

---

## API Endpoints

### Accounts & Balance
- `GET /api/users/{user_id}/accounts` - Get all accounts
- `GET /api/accounts/{account_number}/balance` - Get account balance

### Transactions
- `GET /api/users/{user_id}/transactions?limit=10` - Get recent transactions
- `POST /api/transfer` - Transfer money
- `POST /api/pay-bill` - Pay bills

### Loans & Credit
- `GET /api/loans` - Get loan products
- `GET /api/users/{user_id}/loan-eligibility` - Check eligibility
- `GET /api/users/{user_id}/credit-limit` - Get credit limit

### Other
- `GET /api/users/{user_id}/bills` - Get pending bills
- `GET /api/users/{user_id}/contacts` - Get saved contacts
- `GET /api/interest-rates` - Get interest rates

---

## Test API

### Using curl
```bash
# Get accounts
curl http://localhost:8000/api/users/rahul_sharma/accounts

# Get balance
curl http://localhost:8000/api/accounts/4421/balance

# Get transactions
curl http://localhost:8000/api/users/rahul_sharma/transactions

# Transfer money
curl -X POST http://localhost:8000/api/transfer \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "4421",
    "to_contact": "Anjali Verma",
    "amount": 500,
    "pin": "1234"
  }'
```

### Using Browser
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Test Endpoints**: http://localhost:8000/redoc

---

## Benefits

### Professional Architecture
- Separation of concerns (agent vs data)
- RESTful API design
- Proper error handling

### Production-Ready Design
- Agent calls banking API in real-time
- Shows scalability potential
- Production-like architecture

### Easy to Extend
- Add new endpoints easily
- Modify data without changing agent
- Can connect to real banking APIs later

---

## Current Status

**Option 1: Hardcoded Data**
- Simple, works now
- Less realistic
- Not scalable

**Option 2: Mock API (Recommended)**
- More professional
- Shows real architecture
- Production-ready design
- Takes 30 min to integrate

---

## Next Steps

If you want to integrate the Mock API with the agent:

1. **Update agent.py** to call API instead of using hardcoded data
2. **Add API client** functions
3. **Test** the integration

The Mock API is ready to use.

