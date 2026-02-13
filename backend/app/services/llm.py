import os
from typing import Dict, Any
from fastapi import HTTPException
from openai import OpenAI
from app.agents import run_agent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response(query: str, history: list = None) -> str:
    """
    Process a query through the multi-agent system.

    Args:
        query: The user's question/request
        history: Optional conversation history

    Returns:
        The agent's response string
    """
    try:
        result = run_agent(query, history)

        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error occurred")
            )

        return result.get("response", "No response generated")

    except HTTPException:
        raise
    except Exception as e:
        print(f"[Agent Error]: {e}")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")


def get_response_with_metadata(query: str, history: list = None) -> Dict[str, Any]:
    """
    Process a query and return full metadata about the agent execution.

    Args:
        query: The user's question/request
        history: Optional conversation history

    Returns:
        Dict with response and metadata (query_type, agent_used, plan, etc.)
    """
    try:
        result = run_agent(query, history)

        if not result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Unknown error occurred")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        print(f"[Agent Error]: {e}")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")


def generate_session_title(user_message: str, assistant_response: str) -> str:
    """
    Generate a concise, descriptive title for a chat session based on the conversation content.

    Args:
        user_message: The user's first message
        assistant_response: The assistant's response

    Returns:
        A short title (3-6 words) summarizing the conversation topic
    """
    try:
        system_prompt = """Generate a very short, concise title (3-6 words max) for this conversation.
The title should capture the main topic or intent.
Do NOT use quotes around the title.
Do NOT include words like "Chat about" or "Discussion on".
Just provide the topic directly.

Examples:
- "Python List Sorting"
- "Photo Editing Tips"
- "Morning Greeting"
- "Quantum Physics Basics"
- "Recipe for Pasta"
"""

        content = f"User asked: {user_message}\n\nAssistant replied: {assistant_response[:200]}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.3,
            max_tokens=20
        )

        title = response.choices[0].message.content.strip()
        # Remove quotes if present
        title = title.strip('"\'')
        # Limit length
        if len(title) > 50:
            title = title[:47] + "..."
        return title

    except Exception as e:
        print(f"[Title Generation Error]: {e}")
        # Fallback to simple title from user message
        return user_message[:50] + ("..." if len(user_message) > 50 else "")
