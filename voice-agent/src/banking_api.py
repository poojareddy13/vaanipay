"""
Banking API Client
Handles all communication with the Mock Banking API
"""

import httpx
import logging
from typing import Optional, Dict, List

logger = logging.getLogger("banking-api-client")

class BankingAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.user_id: Optional[str] = None  # User ID must be set via get_user_by_account or set_user_id
    
    def set_user_id(self, user_id: str) -> None:
        """Set the user_id for this client instance"""
        self.user_id = user_id
        logger.info(f"User ID set to: {user_id}")
    
    async def get_user_by_account(self, account_number: str) -> Optional[Dict]:
        """Find user_id by account number and update client user_id"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/accounts/{account_number}/user")
                if response.status_code == 200:
                    user_data = response.json()
                    self.user_id = user_data["user_id"]  # Update user_id
                    logger.info(f"Detected user {self.user_id} from account {account_number}")
                    return user_data
                return None
        except Exception as e:
            logger.error(f"Error finding user by account: {e}")
            return None
    
    def _require_user_id(self) -> None:
        """Raise error if user_id is not set"""
        if self.user_id is None:
            raise ValueError("user_id must be set before making user-specific API calls. Call get_user_by_account() or set_user_id() first.")
        
    async def get_accounts(self) -> List[Dict]:
        """Get all accounts for user"""
        self._require_user_id()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/users/{self.user_id}/accounts")
                if response.status_code == 200:
                    return response.json()["accounts"]
                return []
        except Exception as e:
            logger.error(f"Error getting accounts: {e}")
            return []
    
    async def get_balance(self, account_number: str) -> Optional[Dict]:
        """Get balance for specific account. Auto-detects user if not set."""
        # Auto-detect user from account if not already set
        if self.user_id is None:
            await self.get_user_by_account(account_number)
        
        try:
            async with httpx.AsyncClient() as client:
                # user_id is optional for balance endpoint, but we include it if available
                params = {}
                if self.user_id:
                    params["user_id"] = self.user_id
                response = await client.get(
                    f"{self.base_url}/api/accounts/{account_number}/balance",
                    params=params
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            return None
    
    async def get_transactions(self, limit: int = 10) -> List[Dict]:
        """Get recent transactions"""
        self._require_user_id()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/users/{self.user_id}/transactions",
                    params={"limit": limit}
                )
                if response.status_code == 200:
                    return response.json()["transactions"]
                return []
        except Exception as e:
            logger.error(f"Error getting transactions: {e}")
            return []
    
    async def get_bills(self) -> List[Dict]:
        """Get pending bills"""
        self._require_user_id()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/users/{self.user_id}/bills")
                if response.status_code == 200:
                    return response.json()["bills"]
                return []
        except Exception as e:
            logger.error(f"Error getting bills: {e}")
            return []
    
    async def get_contacts(self) -> List[Dict]:
        """Get saved contacts"""
        self._require_user_id()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/users/{self.user_id}/contacts")
                if response.status_code == 200:
                    return response.json()["contacts"]
                return []
        except Exception as e:
            logger.error(f"Error getting contacts: {e}")
            return []
    
    async def get_loans(self) -> List[Dict]:
        """Get available loan products"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/loans")
                if response.status_code == 200:
                    return response.json()["loan_products"]
                return []
        except Exception as e:
            logger.error(f"Error getting loans: {e}")
            return []
    
    async def get_credit_limit(self) -> Optional[Dict]:
        """Get credit limit information"""
        self._require_user_id()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/users/{self.user_id}/credit-limit")
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error getting credit limit: {e}")
            return None
    
    async def get_interest_rates(self) -> Optional[Dict]:
        """Get current interest rates"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/interest-rates")
                if response.status_code == 200:
                    return response.json()["interest_rates"]
                return None
        except Exception as e:
            logger.error(f"Error getting interest rates: {e}")
            return None
    
    async def transfer_money(self, from_account: str, to_contact: str, amount: float, pin: str) -> Optional[Dict]:
        """Transfer money to contact"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/transfer",
                    json={
                        "from_account": from_account,
                        "to_contact": to_contact,
                        "amount": amount,
                        "pin": pin
                    }
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error transferring money: {e}")
            return None
    
    async def pay_bill(self, account: str, biller: str, amount: float, pin: str) -> Optional[Dict]:
        """Pay a bill"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/pay-bill",
                    json={
                        "account": account,
                        "biller": biller,
                        "amount": amount,
                        "pin": pin
                    }
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error(f"Error paying bill: {e}")
            return None
    
    async def check_api_health(self) -> bool:
        """Check if API is reachable"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API health check failed: {e}")
            return False

