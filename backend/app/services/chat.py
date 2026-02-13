from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import ChatSession, ChatMessage


def create_session(db: Session, user_id: str, title: str = "New Chat") -> ChatSession:
    """Create a new chat session for a user."""
    session = ChatSession(user_id=user_id, title=title)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: str, user_id: str) -> Optional[ChatSession]:
    """Get a chat session by ID, ensuring it belongs to the user."""
    return db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == user_id
    ).first()


def get_user_sessions(db: Session, user_id: str) -> List[ChatSession]:
    """Get all chat sessions for a user, ordered by most recent."""
    return db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(ChatSession.updated_at.desc()).all()


def update_session_title(db: Session, session_id: str, user_id: str, title: str) -> Optional[ChatSession]:
    """Update the title of a chat session."""
    session = get_session(db, session_id, user_id)
    if session:
        session.title = title
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(session)
    return session


def delete_session(db: Session, session_id: str, user_id: str) -> bool:
    """Delete a chat session and all its messages."""
    session = get_session(db, session_id, user_id)
    if session:
        db.delete(session)
        db.commit()
        return True
    return False


def add_message(
    db: Session,
    session_id: str,
    role: str,
    content: str,
    query_type: Optional[str] = None,
    agent_used: Optional[str] = None,
    plan: Optional[List[str]] = None
) -> ChatMessage:
    """Add a message to a chat session."""
    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content,
        query_type=query_type,
        agent_used=agent_used,
        plan=plan
    )
    db.add(message)

    # Update session's updated_at timestamp
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        session.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(message)
    return message


def get_session_messages(db: Session, session_id: str) -> List[ChatMessage]:
    """Get all messages for a chat session, ordered by creation time."""
    return db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()


def get_session_history(db: Session, session_id: str) -> List[dict]:
    """Get chat history in the format expected by the LLM."""
    messages = get_session_messages(db, session_id)
    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]


def generate_session_title(first_message: str) -> str:
    """Generate a title from the first message of a chat."""
    # Take first 50 characters and clean up
    title = first_message[:50].strip()
    if len(first_message) > 50:
        title += "..."
    return title or "New Chat"
