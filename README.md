# VaaniPay - Voice-Enabled Banking Assistant

[![LiveKit](https://img.shields.io/badge/LiveKit-Agents-blue)](https://livekit.io/agents)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![Sarvam AI](https://img.shields.io/badge/Sarvam-AI-orange)](https://sarvam.ai/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-yellow)](https://ai.google.dev/)

VaaniPay is an advanced voice-enabled banking assistant that enables seamless, multilingual banking operations through natural conversation in 11 Indian languages. Built with LiveKit Agents, it provides secure, hands-free banking experiences for Indian users.

## Features

- **Multilingual Support**: 11 Indian languages (English, Hindi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Marathi, Punjabi, Odia)
- **Script Matching Intelligence**: Automatically detects and responds in user's exact script (Native vs Roman)
- **Secure Banking Operations**: PIN-verified transactions with 3-attempt lockout
- **Natural Voice Interaction**: Real-time STT/TTS with Indian accent optimization
- **Comprehensive Banking**: Balance checks, transfers, bill payments, loan inquiries, transaction history

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+ and pnpm
- LiveKit account ([sign up here](https://cloud.livekit.io))
- Sarvam AI API key ([get here](https://www.sarvam.ai))
- Google Gemini API key ([get here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone and setup environment**

```bash
# Clone the repository
git clone <your-repo-url>
cd test-agent

# Set up backend
cd voice-agent
cp .env.example .env.local
# Edit .env.local with your API keys

# Set up frontend
cd ../frontend
cp .env.example .env.local
# Edit .env.local with your LiveKit credentials
```

2. **Install dependencies**

```bash
# Backend (from voice-agent/)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync

# Frontend (from frontend/)
pnpm install
```

### Running the Application

You need **3 terminals** running simultaneously:

**Terminal 1: Mock Banking API**
```bash
cd voice-agent
uv run python mock_banking_api.py
# Verify: http://localhost:8000 shows API info
```

**Terminal 2: Voice Agent**
```bash
cd voice-agent
uv run python src/agent.py dev
# Wait for: "registered worker" message
```

**Terminal 3: Frontend**
```bash
cd frontend
pnpm dev
# Access: http://localhost:3000
```

## Project Structure

```
test-agent/
├── voice-agent/                     # Backend voice agent
│   ├── src/
│   │   ├── agent.py                 # Main voice agent logic
│   │   └── banking_api.py           # Banking API client
│   ├── mock_banking_api.py          # Mock banking service
│   ├── .env.example                 # Backend environment template
│   └── README.md                    # Backend documentation
│
├── frontend/                        # Next.js frontend
│   ├── app/                         # Next.js app directory
│   ├── components/                  # React components
│   ├── .env.example                 # Frontend environment template
│   └── README.md                    # Frontend documentation
│
└── Documentation/
    ├── README.md                                        # This file
    ├── VaaniPay_Project_Technical_Documentation.md     # Technical deep-dive
    ├── VaaniPay.md                                     # Detailed prototype writeup
    ├── DEMO_SCRIPT.md                                  # Demo presentation guide
    └── COMPLETE_TEST_REPORT.md                         # Testing documentation
```

## Architecture

VaaniPay follows a microservices architecture:

1. **Frontend (Next.js)**: User interface with LiveKit client
2. **Voice Agent (Python)**: Real-time voice processing with LiveKit Agents
3. **Mock Banking API (FastAPI)**: RESTful API for banking operations
4. **LiveKit Cloud**: Real-time communication infrastructure

### Technology Stack

- **Speech-to-Text**: Sarvam AI Saarika v2.5 (auto-language detection)
- **Language Model**: Google Gemini 2.5 Flash (multilingual understanding)
- **Text-to-Speech**: Sarvam AI Bulbul v2 (11 Indian languages)
- **Voice Activity Detection**: Silero VAD (optimized for first-speech detection)
- **Real-time Communication**: LiveKit (WebRTC)
- **Backend Framework**: FastAPI (async Python)
- **Frontend Framework**: Next.js 15 (React)

## Configuration

### Environment Variables

**Backend (`voice-agent/.env.local`)**
- `LIVEKIT_URL`: LiveKit server URL
- `LIVEKIT_API_KEY`: LiveKit API key
- `LIVEKIT_API_SECRET`: LiveKit API secret
- `SARVAM_API_KEY`: Sarvam AI API key
- `GEMINI_API_KEY`: Google Gemini API key
- `LLM_PROVIDER`: Choose `gemini` or `groq`
- `BANKING_API_URL`: Mock API URL (default: http://localhost:8000)

**Frontend (`frontend/.env.local`)**
- `LIVEKIT_API_KEY`: Same as backend
- `LIVEKIT_API_SECRET`: Same as backend
- `LIVEKIT_URL`: Same as backend

## Demo Users

The mock banking API includes 4 test users:

| User | Account | PIN | Balance |
|------|---------|-----|---------|
| Rahul Sharma | 4421 | 1234 | ₹27,940 |
| Priya Singh | 9920 | 5678 | ₹156,780 |
| Arjun Reddy | 3366 | 9999 | ₹89,250 |
| Lakshmi Iyer | 7788 | 4444 | ₹213,500 |

## Documentation

- **[Technical Documentation](VaaniPay_Project_Technical_Documentation.md)**: Complete technical architecture and implementation details
- **[Prototype Writeup](VaaniPay.md)**: Detailed explanation of working prototype and real-world applications (~2000 words)
- **[Demo Script](DEMO_SCRIPT.md)**: Step-by-step guide for showcasing all capabilities
- **[Test Report](COMPLETE_TEST_REPORT.md)**: Comprehensive testing documentation
- **[Backend README](voice-agent/README.md)**: Agent development guide
- **[Frontend README](frontend/README.md)**: Frontend development guide
- **[Mock API Guide](voice-agent/MOCK_API_README.md)**: Banking API documentation

## Development

### Running Tests

```bash
cd voice-agent
uv run pytest
```

### Code Formatting

```bash
cd voice-agent
uv run ruff format
uv run ruff check
```

### Hot Reload

The agent automatically reloads when you edit `agent.py` in development mode.

## Troubleshooting

### "Agent did not join the room"
- Ensure Mock API is running (http://localhost:8000)
- Verify voice agent shows "registered worker" message
- Check all API keys are correct in `.env.local`

### First utterance not detected
- The agent uses optimized VAD settings for quick detection
- Speak clearly after connecting
- Check microphone permissions in browser

### Audio cutoff at beginning
- VAD is configured with 200ms prefix padding
- Ensure stable internet connection
- Try refreshing the page

### Language switching issues
- Agent dynamically detects script (Devanagari vs Roman)
- Stick to one language/script per conversation
- Refresh page to start fresh conversation

## Contributing

This is a prototype project. For production use:
- Replace mock API with real banking backend
- Implement proper authentication and authorization
- Add comprehensive audit logging
- Enhance security measures
- Deploy with proper monitoring and alerting




## Acknowledgments

- Built with [LiveKit Agents](https://docs.livekit.io/agents)
- Powered by [Sarvam AI](https://sarvam.ai) for Indian language processing
- LLM by [Google Gemini](https://ai.google.dev/)

---

