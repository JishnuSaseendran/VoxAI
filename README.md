# VoxAI - Multi-Agent AI Voice Assistant

A full-stack multi-agent AI assistant that handles voice and text queries using specialized AI agents, with a Flutter mobile app, Svelte web frontend, and Python backend.

## Overview

VoxAI is an intelligent system that routes your questions to specialized AI agents based on the query type. Whether you need help with coding, math, grammar, research, or just want to chat, the system automatically selects the best agent for your needs.

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Client Applications                        │
│  ┌─────────────────────────┐    ┌────────────────────────────┐   │
│  │   Flutter Mobile App    │    │     Svelte Web Frontend    │   │
│  │   (Android / Cross)     │    │   (Rich UX + Live Status)  │   │
│  └───────────┬─────────────┘    └─────────────┬──────────────┘   │
│              │                                 │                   │
└──────────────┼─────────────────────────────────┼──────────────────┘
               │            REST API             │
               └────────────────┬────────────────┘
                                │
┌───────────────────────────────┼───────────────────────────────────┐
│                           Backend                                  │
│  ┌────────────────────────────┴──────────────────────────────┐    │
│  │                      FastAPI Server                        │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐   │    │
│  │  │   Google STT  │  │   Router     │  │   gTTS (TTS)   │   │    │
│  │  │   + pydub     │  │   Agent      │  │                │   │    │
│  │  └──────────────┘  └──────┬───────┘  └────────────────┘   │    │
│  │                           │                                │    │
│  │  ┌────────────────────────┴────────────────────────────┐   │    │
│  │  │             LangGraph Multi-Agent System             │   │    │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │   │    │
│  │  │  │ General │ │ Coding  │ │ Grammar │ │ Research │  │   │    │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └──────────┘  │   │    │
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐  │   │    │
│  │  │  │ Planner │ │Creative │ │  Math   │ │  Chat    │  │   │    │
│  │  │  └─────────┘ └─────────┘ └─────────┘ └──────────┘  │   │    │
│  │  └─────────────────────────────────────────────────────┘   │    │
│  └────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────┘
```

## Features

- **Multi-Agent AI** - 8 specialized agents for different query types (powered by OpenAI GPT-4o-mini)
- **Voice Input** - Speak your questions using the microphone
- **Text Input** - Type questions directly
- **Text-to-Speech** - Listen to AI responses via gTTS with playback controls
- **Auto-Routing** - Automatically selects the best agent for your query
- **User Authentication** - JWT-based signup/login to save conversations
- **Chat History** - Session-based chat history with sidebar navigation
- **Mobile App** - Flutter-based Android app with full feature parity
- **Web Frontend** - Svelte app with real-time status updates and responsive design

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
- Flutter SDK 3.0+ (for mobile app)
- FFmpeg (for audio processing)
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

### 2. Web Frontend Setup

```bash
cd frontend-svelte
npm install
npm run dev
```

Frontend runs at `http://localhost:3000`

### 3. Mobile App Setup

```bash
cd android-app
flutter pub get
flutter run
```

See [Android App README](android-app/README.md) for API URL configuration.

## Project Structure

```
Voice-Assistant/
├── backend/                 # FastAPI + LangGraph backend
│   ├── app/
│   │   ├── agents/          # Multi-agent system (router, 8 specialists)
│   │   │   ├── state.py     # Agent state definition
│   │   │   ├── nodes.py     # Agent implementations
│   │   │   └── graph.py     # LangGraph orchestration
│   │   ├── services/        # Auth, chat, LLM, speech services
│   │   │   ├── auth.py      # JWT authentication
│   │   │   ├── chat.py      # Session & message management
│   │   │   ├── llm.py       # OpenAI LLM interface
│   │   │   └── speech.py    # Google STT + gTTS
│   │   ├── database.py      # SQLAlchemy database setup
│   │   ├── models.py        # User, Session, Message models
│   │   └── main.py          # FastAPI endpoints
│   ├── requirements.txt
│   └── README.md
│
├── frontend-svelte/         # Svelte web frontend
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/  # UI components (8 components)
│   │   │   ├── stores/      # Svelte stores (assistant, auth, chat, config)
│   │   │   └── services/    # API service layer
│   │   └── App.svelte
│   └── README.md
│
├── android-app/             # Flutter mobile app
│   ├── lib/
│   │   ├── models/          # Data models (user, session, message)
│   │   ├── providers/       # State management (auth, chat)
│   │   ├── services/        # API client
│   │   ├── screens/         # Splash, login, home screens
│   │   └── widgets/         # Chat drawer, message bubble, status
│   ├── pubspec.yaml
│   └── README.md
│
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
- [Android App Documentation](android-app/README.md) - Mobile setup, features

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | OpenAI GPT-4o-mini |
| **Agent Orchestration** | LangGraph |
| **Backend Framework** | FastAPI |
| **Speech-to-Text** | Google Speech Recognition (via SpeechRecognition) |
| **Text-to-Speech** | gTTS (Google Text-to-Speech) |
| **Audio Processing** | pydub + FFmpeg |
| **Database** | SQLite (via SQLAlchemy) |
| **Authentication** | JWT (python-jose + passlib/bcrypt) |
| **Web Frontend** | Svelte 4 + Vite 5 |
| **Mobile App** | Flutter 3 (Dart) |
| **State Management** | Svelte stores (web), Provider (mobile) |

## License

MIT
