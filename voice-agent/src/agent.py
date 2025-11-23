"""
VaaniPay Voice Banking Agent
Built following Sarvam AI + LiveKit best practices
Reference: https://docs.sarvam.ai/api-reference-docs/cookbook/integration/build-voice-agent-with-live-kit
"""

import logging
import os
import re

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
    vad,
)
from livekit.plugins import groq, sarvam, google, silero
from banking_api import BankingAPIClient

# Set up logging (following Sarvam AI best practices)
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()
load_dotenv(".env.local")  # Also load .env.local for LiveKit credentials

# Initialize Banking API Client
banking_api = BankingAPIClient(base_url=os.getenv("BANKING_API_URL", "http://localhost:8000"))

# Model selection - set in .env.local: LLM_PROVIDER=gemini or groq
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

def sanitize_response(text: str) -> str:
    """
    Remove all technical details, function calls, and tool mentions from LLM responses.
    This ensures users only see natural language, not internal implementation details.
    """
    if not text:
        return text

    # Pattern 1: Remove "Tool: function_name Parameters: {...}" style mentions
    text = re.sub(r'Tool:\s*\w+\s+Parameters:\s*\{[^}]*\}', '', text, flags=re.IGNORECASE)

    # Pattern 2: Remove standalone "Tool:" or "Function:" mentions
    text = re.sub(r'\b(Tool|Function|API|called with|calling|Parameters?):\s*[^\n.]*', '', text, flags=re.IGNORECASE)

    # Pattern 3: Remove JSON-like structures that might be exposed
    text = re.sub(r'\{["\']?\w+["\']?\s*:\s*[^}]{0,100}\}', '', text)

    # Pattern 4: Remove common function names
    function_names = ['get_banking_data', 'transfer_funds', 'pay_bill', 'check_balance']
    for func_name in function_names:
        text = re.sub(rf'\b{func_name}\b', '', text, flags=re.IGNORECASE)

    # Pattern 5: Remove any remaining technical markers
    technical_markers = [
        r'data_type\s*=',
        r'account_number\s*=',
        r'called with',
        r'executing',
        r'running tool',
        r'using function'
    ]
    for marker in technical_markers:
        text = re.sub(marker, '', text, flags=re.IGNORECASE)

    # Clean up extra whitespace and punctuation that may result from removals
    text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove space before punctuation
    text = re.sub(r'\s{2,}', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'^\s+|\s+$', '', text)  # Trim leading/trailing whitespace

    # Remove empty sentences (just punctuation)
    text = re.sub(r'[.!?]\s*[.!?]+', '.', text)  # Multiple punctuation to single

    logger.debug(f"Sanitized text: {text}")
    return text


class VoiceAgent(Agent):
    def __init__(self) -> None:
        # Select LLM based on environment variable
        if LLM_PROVIDER == "gemini":
            llm_instance = google.LLM(
                model="gemini-2.5-flash",  # Latest Gemini 2.5 Flash model
                # Gemini 2.5 Flash: Enhanced multilingual understanding, improved for banking conversations
            )
            logger.info("Using Gemini 2.5 Flash for LLM")
        else:
            llm_instance = groq.LLM(
                model="llama-3.1-8b-instant",  # Fast inference
            )
            logger.info("Using Groq Llama 3.1 for LLM")

        # Store detected language for TTS (default to English)
        self.detected_language = "en-IN"
        self.current_language_name = "English"
        self.conversation_language_locked = False  # Lock language after first detection

        super().__init__(
            # Your agent's personality and instructions
            instructions="""You are VaaniPay, a helpful voice banking assistant for Indian users.

IMPORTANT RULES:
1. Wait for user to speak first - never greet or introduce yourself
2. Detect the language from user's first message (Hindi, Telugu, Tamil, English, etc.)
3. Continue the ENTIRE conversation in that same language - never switch languages mid-conversation
4. Be professional, warm, and concise
5. Always confirm important actions before executing them

Available banking functions:
- Check account balance
- View recent transactions
- Pay bills
- Send money to contacts
- Get loan information

Example conversation flows:

Balance check:
User: "What's my balance?" or "मेरा बैलेंस बताइए"
You: "Could you provide your account number?" (in their language)
User: "4421"
You: Fetch balance and respond "Your account 4421 has 27,940 rupees"

Send money:
User: "Send 500 to Anjali" or "अंजली को 500 भेजो"
You: "Alright, transfer 500 rupees to Anjali Verma. Is that correct?" (in their language)
User: "Yes"
You: "Please enter your PIN" (in their language)
User: (types PIN - user never speaks PIN, they type it silently)
You: If PIN is "1234" - confirm "PIN is correct" and process transfer "Transaction successful. 500 rupees sent to Anjali"
     If PIN is wrong - say "PIN incorrect. Please try again"
     If wrong 3 times - say "Three wrong attempts. Account blocked"

Loan inquiry:
User: "What are the loan interest rates?" or "लोन की ब्याज दर क्या है?"
You: Fetch loan data and respond "Personal loan is 10.5% per year, home loan is 8.25% per year, car loan is 9% per year"
""",
            # Saarika STT - Converts speech to text
            stt=sarvam.STT(
                language="unknown",  # Auto-detect language
                model="saarika:v2.5"
            ),
            # LLM - The "brain" that processes and generates responses
            llm=llm_instance,  # Gemini or Groq based on LLM_PROVIDER
            # Bulbul TTS - Converts text to speech
            # Note: We'll update TTS language dynamically based on detected user language
            # Starting with en-IN (English) as default, but will switch based on conversation
            tts=sarvam.TTS(
                target_language_code="en-IN",  # Default to English, will be updated dynamically
                model="bulbul:v2",
                speaker="manisha"
            ),
            # Silero VAD - Optimized settings for better first-speech detection
            vad=silero.VAD.load(
                min_speech_duration=0.1,  # Detect speech after 100ms (faster response)
                min_silence_duration=0.5,  # Wait 500ms of silence before ending turn
                prefix_padding_duration=0.2,  # Include 200ms before speech starts
                max_buffered_speech=30.0  # Buffer up to 30s of speech
            ),
        )
    
    async def get_banking_data(self, data_type: str, **kwargs) -> str:
        """
        Fetch banking data from API and format for LLM.
        
        Args:
            data_type: Type of data to fetch (accounts, balance, transactions, bills, loans, etc.)
            **kwargs: Additional parameters like account_number, limit, etc.
        
        Returns:
            Formatted string with the requested data
        """
        try:
            if data_type == "loans":
                loans = await banking_api.get_loans()
                if loans:
                    # Format loans with explicit fixed rates
                    formatted = []
                    for loan in loans:
                        formatted.append(
                            f"{loan['type']}: Fixed rate {loan['interest_rate']}% per year, "
                            f"maximum amount ₹{loan['max_amount']:,}, "
                            f"tenure {loan['min_tenure']} to {loan['max_tenure']} {loan['unit']}"
                        )
                    return "\n".join(formatted)
            
            elif data_type == "accounts":
                # Try to get user from account number if provided
                account_number = kwargs.get("account_number")
                if account_number:
                    user_data = await banking_api.get_user_by_account(account_number)
                    if user_data:
                        logger.info(f"Found user {user_data['user_id']} for account {account_number}")
                
                # If no user_id set, we can't get accounts - return helpful message
                if banking_api.user_id is None:
                    return "Please provide an account number so I can identify your accounts."
                
                accounts = await banking_api.get_accounts()
                if accounts:
                    return "\n".join([
                        f"- {acc['account_number']} ({acc['account_type']}): ₹{acc['balance']:,.0f}"
                        for acc in accounts
                    ])
            
            elif data_type == "balance":
                account = kwargs.get("account_number")
                # If account number is provided, find the user first
                if account:
                    user_data = await banking_api.get_user_by_account(account)
                    if user_data:
                        logger.info(f"Found user {user_data['user_id']} for account {account}")
                
                balance_data = await banking_api.get_balance(account)
                if balance_data:
                    return f"Account {balance_data['account_number']}: ₹{balance_data['balance']:,.0f}"
            
            elif data_type == "transactions":
                account_number = kwargs.get("account_number")
                if account_number:
                    user_data = await banking_api.get_user_by_account(account_number)
                    if user_data:
                        logger.info(f"Found user {user_data['user_id']} for account {account_number}")
                
                transactions = await banking_api.get_transactions(limit=10)
                if transactions:
                    formatted = []
                    for txn in transactions:
                        amount = f"₹{txn['amount']:,.0f}"
                        formatted.append(f"{txn['date']}: {amount} - {txn['description']}")
                    return "\n".join(formatted)
            
            elif data_type == "bills":
                account_number = kwargs.get("account_number")
                if account_number:
                    user_data = await banking_api.get_user_by_account(account_number)
                    if user_data:
                        logger.info(f"Found user {user_data['user_id']} for account {account_number}")
                
                bills = await banking_api.get_bills()
                if bills:
                    return "\n".join([
                        f"{bill['biller']}: ₹{bill['amount']:,.0f} (due: {bill['due_date']})"
                        for bill in bills if bill['status'] == 'pending'
                    ])
            
            elif data_type == "contacts":
                contacts = await banking_api.get_contacts()
                if contacts:
                    return "\n".join([f"- {c['name']}" for c in contacts])
            
            return "API data temporarily unavailable, using fallback data"
            
        except Exception as e:
            logger.error(f"Error fetching {data_type}: {e}")
            return "Using fallback data due to API error"
    
    async def on_user_speech_committed(self, message):
        """
        Called when user's speech is transcribed.
        Detect language and lock it for the entire conversation, update TTS accordingly.
        """
        # Language code mapping from detected text
        text = message.content if hasattr(message, 'content') else str(message)

        # Language name mapping for LLM instructions
        language_names = {
            "hi-IN": "Hindi",
            "te-IN": "Telugu",
            "gu-IN": "Gujarati",
            "ta-IN": "Tamil",
            "kn-IN": "Kannada",
            "ml-IN": "Malayalam",
            "bn-IN": "Bengali",
            "pa-IN": "Punjabi",
            "od-IN": "Odia",
            "en-IN": "English"
        }

        # Simple language detection based on script
        if any('\u0900' <= char <= '\u097F' for char in text):  # Devanagari (Hindi)
            new_lang = "hi-IN"
        elif any('\u0C00' <= char <= '\u0C7F' for char in text):  # Telugu
            new_lang = "te-IN"
        elif any('\u0A80' <= char <= '\u0AFF' for char in text):  # Gujarati
            new_lang = "gu-IN"
        elif any('\u0B80' <= char <= '\u0BFF' for char in text):  # Tamil
            new_lang = "ta-IN"
        elif any('\u0C80' <= char <= '\u0CFF' for char in text):  # Kannada
            new_lang = "kn-IN"
        elif any('\u0D00' <= char <= '\u0D7F' for char in text):  # Malayalam
            new_lang = "ml-IN"
        elif any('\u0980' <= char <= '\u09FF' for char in text):  # Bengali
            new_lang = "bn-IN"
        elif any('\u0A00' <= char <= '\u0A7F' for char in text):  # Punjabi
            new_lang = "pa-IN"
        elif any('\u0B00' <= char <= '\u0B7F' for char in text):  # Odia
            new_lang = "od-IN"
        else:  # English or Roman script
            new_lang = "en-IN"

        # On first user message, lock the language for the entire conversation
        if not self.conversation_language_locked:
            self.detected_language = new_lang
            self.current_language_name = language_names.get(new_lang, "English")
            self.conversation_language_locked = True
            logger.info(f"Language LOCKED to: {new_lang} ({self.current_language_name}) for entire conversation")
            
            # Update the TTS instance
            self.tts = sarvam.TTS(
                target_language_code=new_lang,
                model="bulbul:v2",
                speaker="manisha"
            )
            
            # Update the STT to use the detected language for better accuracy
            self.stt = sarvam.STT(
                language=new_lang,  # Set specific language instead of "unknown"
                model="saarika:v2.5"
            )
        
        # Prepend language reminder to message content if language is locked
        if self.conversation_language_locked and hasattr(message, 'content'):
            # Add language enforcement to the message
            original_content = message.content
            message.content = f"[IMPORTANT: Respond in {self.current_language_name} only] {original_content}"
            logger.debug(f"Prepended language reminder to message: {self.current_language_name}")

        return await super().on_user_speech_committed(message)

    async def on_enter(self):
        """Called when user joins - prime the VAD and wait for user to speak first"""
        # Log connection but don't speak - just ensure VAD is ready
        logger.info("Agent ready, VAD primed, waiting for user speech")
        # Do NOT generate reply - wait for user to speak
        pass


async def entrypoint(ctx: JobContext):
    """
    Main entry point - LiveKit calls this when a user connects
    Following Sarvam AI best practices from:
    https://docs.sarvam.ai/api-reference-docs/cookbook/integration/build-voice-agent-with-live-kit
    """
    try:
        logger.info(f"User connected to room: {ctx.room.name}")
        
        # CRITICAL: Accept the job first to prevent timeout
        await ctx.connect()
        
        # Create and start the agent session
        session = AgentSession()
        await session.start(
            agent=VoiceAgent(),
            room=ctx.room
        )
    except Exception as e:
        logger.error(f"Error in entrypoint: {e}")
        raise


if __name__ == "__main__":
    # Run the agent - no agent_name to enable auto-dispatch
    cli.run_app(WorkerOptions(
        entrypoint_fnc=entrypoint
    ))
