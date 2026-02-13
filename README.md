# Voice Assistant

A full-stack multi-agent AI assistant that handles voice and text queries using specialized AI agents.

## Overview

Voice Assistant is an intelligent system that routes your questions to specialized AI agents based on the query type. Whether you need help with coding, math, grammar, research, or just want to chat, the system automatically selects the best agent for your needs.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Options                          │
│  ┌─────────────────────┐       ┌─────────────────────────────┐  │
│  │   Vanilla JS        │       │        Svelte               │  │
│  │   (Zero deps)       │       │    (Rich UX + Live Status)  │  │
│  └──────────┬──────────┘       └──────────────┬──────────────┘  │
│             │                                  │                  │
└─────────────┼──────────────────────────────────┼─────────────────┘
              │          REST API                │
              └──────────────┬───────────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                        Backend                                   │
│  ┌─────────────────────────┴─────────────────────────────────┐  │
│  │                     FastAPI Server                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │  │
│  │  │   Speech    │  │   Router    │  │   Text-to-Speech│    │  │
│  │  │   Service   │  │   Agent     │  │   Service       │    │  │
│  │  └─────────────┘  └──────┬──────┘  └─────────────────┘    │  │
│  │                          │                                 │  │
│  │  ┌───────────────────────┴───────────────────────────┐    │  │
│  │  │              LangGraph Multi-Agent System          │    │  │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │    │  │
│  │  │  │ General │ │ Coding  │ │ Grammar │ │Research │  │    │  │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │    │  │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │    │  │
│  │  │  │ Planner │ │Creative │ │  Math   │ │  Chat   │  │    │  │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │    │  │
│  │  └───────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Features

- **Multi-Agent AI** - Specialized agents for different query types
- **Voice Input** - Speak your questions using the microphone
- **Text Input** - Type questions directly
- **Text-to-Speech** - Listen to AI responses with playback controls
- **Auto-Routing** - Automatically selects the best agent for your query
- **User Authentication** - Sign up and login to save your conversations
- **Chat History** - Session-based chat history with sidebar navigation
- **Two Frontend Options** - Choose between lightweight vanilla JS or feature-rich Svelte

## Specialized Agents

| Agent | Purpose | Example Query |
|-------|---------|---------------|
| General | Knowledge & explanations | "What is photosynthesis?" |
| Coding | Programming help | "Write a Python function to sort a list" |
| Grammar | Text correction | "Fix this sentence: Me go store" |
| Research | Deep analysis | "Compare React vs Vue for large apps" |
| Planner | Task breakdown | "Plan a website development project" |
| Creative | Content creation | "Write a poem about the ocean" |
| Math | Calculations | "Solve: 2x + 5 = 15" |
| Conversation | Casual chat | "Hello, how are you?" |

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+ (for Svelte frontend)
- FFmpeg
- OpenAI API key

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Start server
python run.py
```

Backend runs at `http://localhost:8000`

### 2. Frontend Setup

**Option A: Svelte (Recommended for rich UX)**

```bash
cd frontend-svelte
npm install
npm run dev
```

**Option B: Vanilla JS (Zero dependencies)**

```bash
cd frontend
python -m http.server 3000
```

Frontend runs at `http://localhost:3000`

## Project Structure

```
Voice-Assistant/
├── backend/                 # FastAPI + LangGraph backend
│   ├── app/
│   │   ├── agents/          # Multi-agent system
│   │   ├── services/        # Speech & LLM services
│   │   └── main.py          # API endpoints
│   ├── requirements.txt
│   └── README.md
│
├── frontend-svelte/         # Modern Svelte frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # UI components
│   │   │   ├── stores/      # State management
│   │   │   └── services/    # API services
│   │   └── App.svelte
│   └── README.md
│
└── frontend/                # Vanilla JS frontend
    ├── index.html
    ├── css/style.css
    ├── js/app.js
    └── README.md
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/auth/signup` | POST | Register new user |
| `/api/auth/login` | POST | Login user |
| `/api/auth/me` | GET | Get current user |
| `/api/sessions` | GET | List user's chat sessions |
| `/api/sessions` | POST | Create new chat session |
| `/api/sessions/{id}` | GET | Get session with messages |
| `/api/sessions/{id}` | PATCH | Update session title |
| `/api/sessions/{id}` | DELETE | Delete session |
| `/api/ask/text` | POST | Text query |
| `/api/ask/text/detailed` | POST | Text query with agent info |
| `/api/ask/voice` | POST | Voice query |
| `/api/ask/voice/detailed` | POST | Voice query with agent info |
| `/api/tts` | POST | Text-to-speech |
| `/api/agents` | GET | List available agents |

## Documentation

- [Backend Documentation](backend/README.md) - API details, agent system, setup
- [Svelte Frontend Documentation](frontend-svelte/README.md) - Components, state management
- [Vanilla JS Frontend Documentation](frontend/README.md) - Simple setup, customization

## Technology Stack

**Backend**
- FastAPI - Web framework
- LangGraph - Multi-agent orchestration
- OpenAI - GPT models & Whisper STT
- FFmpeg - Audio processing

**Frontend (Svelte)**
- Svelte - Reactive framework
- Vite - Build tool

**Frontend (Vanilla)**
- HTML/CSS/JavaScript - No dependencies

## License

MIT
