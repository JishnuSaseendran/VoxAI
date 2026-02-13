import os
import tempfile
from typing import Optional, List
from datetime import timedelta
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

from app.database import get_db, init_db
from app.models import User, ChatSession, ChatMessage
from app.services.llm import get_response, get_response_with_metadata, generate_session_title
from app.services.speech import transcribe_audio, text_to_speech
from app.services.auth import (
    create_user, authenticate_user, create_access_token,
    get_current_user, get_optional_user, get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.services.chat import (
    create_session, get_session, get_user_sessions,
    update_session_title, delete_session, add_message,
    get_session_messages, get_session_history
)

app = FastAPI(
    title="Voice Assistant API - Multi-Agent System",
    description="AI-powered voice assistant with specialized agents for different query types",
    version="2.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# ============== Request/Response Models ==============

class TextQuestion(BaseModel):
    question: str
    session_id: Optional[str] = None


class AnswerResponse(BaseModel):
    question: str
    answer: str


class DetailedAnswerResponse(BaseModel):
    question: str
    answer: str
    query_type: Optional[str] = None
    agent_used: Optional[str] = None
    plan: Optional[List[str]] = None
    session_id: Optional[str] = None
    session_title: Optional[str] = None
    message_id: Optional[str] = None


# Auth Models
class UserSignup(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Chat Session Models
class SessionCreate(BaseModel):
    title: Optional[str] = "New Chat"


class SessionUpdate(BaseModel):
    title: str


class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    query_type: Optional[str] = None
    agent_used: Optional[str] = None
    plan: Optional[List[str]] = None
    created_at: str


class SessionWithMessagesResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    messages: List[MessageResponse]


# ============== Auth Endpoints ==============

@app.post("/api/auth/signup", response_model=TokenResponse)
async def signup(data: UserSignup, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if email already exists
    existing_user = get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = create_user(db, data.email, data.username, data.password)

    # Create access token
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user.id, email=user.email, username=user.username)
    )


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user.id, email=user.email, username=user.username)
    )


@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username
    )


# ============== Chat Session Endpoints ==============

@app.post("/api/sessions", response_model=SessionResponse)
async def create_chat_session(
    data: SessionCreate = SessionCreate(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    session = create_session(db, current_user.id, data.title)
    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat()
    )


@app.get("/api/sessions", response_model=List[SessionResponse])
async def list_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all chat sessions for the current user."""
    sessions = get_user_sessions(db, current_user.id)
    return [
        SessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at.isoformat(),
            updated_at=s.updated_at.isoformat()
        )
        for s in sessions
    ]


@app.get("/api/sessions/{session_id}", response_model=SessionWithMessagesResponse)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a chat session with all its messages."""
    session = get_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = get_session_messages(db, session_id)
    return SessionWithMessagesResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        messages=[
            MessageResponse(
                id=m.id,
                role=m.role,
                content=m.content,
                query_type=m.query_type,
                agent_used=m.agent_used,
                plan=m.plan,
                created_at=m.created_at.isoformat()
            )
            for m in messages
        ]
    )


@app.patch("/api/sessions/{session_id}", response_model=SessionResponse)
async def update_chat_session(
    session_id: str,
    data: SessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a chat session's title."""
    session = update_session_title(db, session_id, current_user.id, data.title)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat()
    )


@app.delete("/api/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a chat session and all its messages."""
    success = delete_session(db, session_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


# ============== Original Endpoints ==============

@app.get("/")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Voice Assistant Multi-Agent API is running",
        "version": "2.0.0",
        "agents": [
            "router",
            "general",
            "coding",
            "grammar",
            "research",
            "planner",
            "creative",
            "math",
            "conversation"
        ]
    }


@app.post("/api/ask/text", response_model=AnswerResponse)
async def ask_text(data: TextQuestion):
    """Handle text-based questions using the multi-agent system."""
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    print(f"[Query]: {data.question}")
    answer = get_response(data.question)
    print(f"[Response]: {answer[:100]}...")

    return AnswerResponse(question=data.question, answer=answer)


@app.post("/api/ask/text/detailed", response_model=DetailedAnswerResponse)
async def ask_text_detailed(
    data: TextQuestion,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    Handle text-based questions with detailed agent metadata.
    If session_id is provided, saves the conversation to that session.
    """
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    session_id = data.session_id
    history = []
    is_new_session = False

    # If user is authenticated and session_id provided, load history
    if current_user and session_id:
        session = get_session(db, session_id, current_user.id)
        if session:
            history = get_session_history(db, session_id)
        else:
            raise HTTPException(status_code=404, detail="Session not found")

    # Track if we need to create a new session
    if current_user and not session_id:
        is_new_session = True

    print(f"[Query]: {data.question}")
    result = get_response_with_metadata(data.question, history=history)
    print(f"[Agent Used]: {result.get('agent_used')}")
    print(f"[Response]: {result.get('response', '')[:100]}...")

    message_id = None
    session_title = None

    # Create new session with AI-generated title (after we have the response)
    if current_user and is_new_session:
        session_title = generate_session_title(data.question, result.get("response", ""))
        new_session = create_session(db, current_user.id, session_title)
        session_id = new_session.id

    # Save messages to session if authenticated
    if current_user and session_id:
        # Save user message
        add_message(db, session_id, "user", data.question)
        # Save assistant message
        assistant_msg = add_message(
            db, session_id, "assistant", result.get("response", ""),
            query_type=result.get("query_type"),
            agent_used=result.get("agent_used"),
            plan=result.get("plan")
        )
        message_id = assistant_msg.id

    return DetailedAnswerResponse(
        question=data.question,
        answer=result.get("response", ""),
        query_type=result.get("query_type"),
        agent_used=result.get("agent_used"),
        plan=result.get("plan"),
        session_id=session_id,
        session_title=session_title,
        message_id=message_id
    )


@app.post("/api/ask/voice", response_model=AnswerResponse)
async def ask_voice(audio: UploadFile = File(...)):
    """Handle voice-based questions. Supports any audio format."""
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")

    # Get file extension from uploaded file
    ext = os.path.splitext(audio.filename)[1] if audio.filename else ".webm"
    if not ext:
        ext = ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        question = transcribe_audio(tmp_path)

        if not question.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        print(f"[Voice Query]: {question}")
        answer = get_response(question)
        print(f"[Response]: {answer[:100]}...")

        return AnswerResponse(question=question, answer=answer)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/api/ask/voice/detailed", response_model=DetailedAnswerResponse)
async def ask_voice_detailed(
    audio: UploadFile = File(...),
    session_id: Optional[str] = Form(None),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """Handle voice-based questions with detailed agent metadata."""
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")

    ext = os.path.splitext(audio.filename)[1] if audio.filename else ".webm"
    if not ext:
        ext = ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        content = await audio.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        question = transcribe_audio(tmp_path)

        if not question.strip():
            raise HTTPException(status_code=400, detail="Could not transcribe audio")

        history = []
        is_new_session = False

        # If user is authenticated and session_id provided, load history
        if current_user and session_id:
            session = get_session(db, session_id, current_user.id)
            if session:
                history = get_session_history(db, session_id)
            else:
                raise HTTPException(status_code=404, detail="Session not found")

        # Track if we need to create a new session
        if current_user and not session_id:
            is_new_session = True

        print(f"[Voice Query]: {question}")
        result = get_response_with_metadata(question, history=history)
        print(f"[Agent Used]: {result.get('agent_used')}")

        message_id = None
        session_title = None

        # Create new session with AI-generated title (after we have the response)
        if current_user and is_new_session:
            session_title = generate_session_title(question, result.get("response", ""))
            new_session = create_session(db, current_user.id, session_title)
            session_id = new_session.id

        # Save messages to session if authenticated
        if current_user and session_id:
            add_message(db, session_id, "user", question)
            assistant_msg = add_message(
                db, session_id, "assistant", result.get("response", ""),
                query_type=result.get("query_type"),
                agent_used=result.get("agent_used"),
                plan=result.get("plan")
            )
            message_id = assistant_msg.id

        return DetailedAnswerResponse(
            question=question,
            answer=result.get("response", ""),
            query_type=result.get("query_type"),
            agent_used=result.get("agent_used"),
            plan=result.get("plan"),
            session_id=session_id,
            session_title=session_title,
            message_id=message_id
        )
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/api/tts")
async def tts_endpoint(data: TextQuestion):
    """Convert text to speech and return audio file."""
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_buffer = text_to_speech(data.question)
    return StreamingResponse(
        audio_buffer,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=response.mp3"}
    )


@app.get("/api/agents")
async def list_agents():
    """List all available agents and their capabilities."""
    return {
        "agents": [
            {
                "name": "router",
                "description": "Decision agent that analyzes queries and routes to appropriate specialist"
            },
            {
                "name": "general",
                "description": "Handles general knowledge questions and explanations"
            },
            {
                "name": "coding",
                "description": "Expert programmer for code writing, debugging, and technical questions"
            },
            {
                "name": "grammar",
                "description": "Grammar correction and sentence improvement specialist"
            },
            {
                "name": "research",
                "description": "Deep analysis and research for complex topics"
            },
            {
                "name": "planner",
                "description": "Creates step-by-step plans for complex tasks"
            },
            {
                "name": "creative",
                "description": "Creative writing and content generation"
            },
            {
                "name": "math",
                "description": "Mathematical problems and calculations"
            },
            {
                "name": "conversation",
                "description": "Casual conversation and chitchat"
            }
        ]
    }
