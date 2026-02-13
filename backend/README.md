# Voice Assistant Backend

A FastAPI-powered multi-agent AI system that handles voice and text queries using specialized agents.

## Architecture

```
backend/
├── app/
│   ├── agents/
│   │   ├── state.py      # Agent state definition
│   │   ├── nodes.py      # Individual agent implementations
│   │   └── graph.py      # LangGraph orchestration
│   ├── services/
│   │   ├── llm.py        # Multi-agent interface
│   │   └── speech.py     # Speech-to-text & text-to-speech
│   └── main.py           # FastAPI endpoints
├── requirements.txt
├── run.py
└── .env
```

## Multi-Agent System

The system uses LangGraph to orchestrate specialized agents:

| Agent | Purpose | Use Case |
|-------|---------|----------|
| **Router** | Query classification | Analyzes and routes to specialists |
| **General** | Knowledge & facts | "What is photosynthesis?" |
| **Coding** | Programming help | "Write a Python function to sort a list" |
| **Grammar** | Text correction | "Fix this sentence: Me go store" |
| **Research** | Deep analysis | "Compare React vs Vue for large apps" |
| **Planner** | Task breakdown | "Plan a website development project" |
| **Creative** | Content creation | "Write a poem about the ocean" |
| **Math** | Calculations | "Solve: 2x + 5 = 15" |
| **Conversation** | Casual chat | "Hello, how are you?" |

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install FFmpeg (required for audio processing)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
choco install ffmpeg
```

### 3. Configure Environment

Create `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### 4. Run the Server

```bash
python run.py
```

Server starts at `http://localhost:8000`

## API Endpoints

### Authentication

#### Sign Up
```
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "John",
  "password": "yourpassword"
}
```
Returns JWT token and user info.

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword"
}
```
Returns JWT token and user info.

#### Get Current User
```
GET /api/auth/me
Authorization: Bearer <token>
```
Returns current user info.

### Chat Sessions

#### Create Session
```
POST /api/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My Chat"
}
```

#### List Sessions
```
GET /api/sessions
Authorization: Bearer <token>
```
Returns all chat sessions for the user.

#### Get Session with Messages
```
GET /api/sessions/{session_id}
Authorization: Bearer <token>
```
Returns session with all messages.

#### Update Session
```
PATCH /api/sessions/{session_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "New Title"
}
```

#### Delete Session
```
DELETE /api/sessions/{session_id}
Authorization: Bearer <token>
```

### Health Check
```
GET /
```
Returns server status and available agents.

### Text Query
```
POST /api/ask/text
Content-Type: application/json

{
  "question": "Your question here"
}
```

### Text Query (Detailed)
```
POST /api/ask/text/detailed
Content-Type: application/json

{
  "question": "Your question here"
}
```
Returns response with agent metadata (which agent handled the query).

### Voice Query
```
POST /api/ask/voice
Content-Type: multipart/form-data

audio: <audio file>
```
Supports: webm, mp3, wav, ogg, m4a, flac, etc.

### Voice Query (Detailed)
```
POST /api/ask/voice/detailed
Content-Type: multipart/form-data

audio: <audio file>
```

### Text-to-Speech
```
POST /api/tts
Content-Type: application/json

{
  "question": "Text to convert to speech"
}
```
Returns MP3 audio file.

### List Agents
```
GET /api/agents
```
Returns list of all available agents with descriptions.

## Example Usage

### cURL

```bash
# Text query
curl -X POST http://localhost:8000/api/ask/text/detailed \
  -H "Content-Type: application/json" \
  -d '{"question": "Write a hello world in Python"}'

# Voice query
curl -X POST http://localhost:8000/api/ask/voice \
  -F "audio=@recording.webm"

# Text-to-speech
curl -X POST http://localhost:8000/api/tts \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello, this is a test"}' \
  --output response.mp3
```

### Python

```python
import requests

# Text query
response = requests.post(
    "http://localhost:8000/api/ask/text/detailed",
    json={"question": "Explain quantum computing"}
)
data = response.json()
print(f"Agent: {data['agent_used']}")
print(f"Answer: {data['answer']}")
```

## Development

### API Documentation

FastAPI auto-generates documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Adding New Agents

1. Add agent function in `app/agents/nodes.py`
2. Register in `app/agents/graph.py`
3. Update router classification in `router_agent()`

## Requirements

- Python 3.9+
- FFmpeg
- OpenAI API key

## Database

The application uses SQLite by default. The database file `voice_assistant.db` is created automatically in the backend directory on first run.

To use a different database, set the `DATABASE_URL` environment variable:
```env
DATABASE_URL=sqlite:///./voice_assistant.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/voiceassistant
```

## Security

For production, set a secure JWT secret key:
```env
JWT_SECRET_KEY=your-secure-secret-key-here
```
