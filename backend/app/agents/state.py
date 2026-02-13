from typing import TypedDict, Literal, List, Optional


class AgentState(TypedDict):
    """State that flows through the agent graph."""
    # Original user query
    query: str

    # Classification of the query type
    query_type: Optional[str]

    # Selected agent(s) to handle the query
    selected_agent: Optional[str]

    # Plan for complex tasks
    plan: Optional[List[str]]

    # Research/context gathered
    research_context: Optional[str]

    # Refined/corrected query (for grammar fixes)
    refined_query: Optional[str]

    # Final response
    response: Optional[str]

    # Conversation history for context
    history: List[dict]

    # Error message if any
    error: Optional[str]


# Query types that the router can classify
QUERY_TYPES = Literal[
    "general",      # General knowledge questions
    "coding",       # Programming/code related
    "grammar",      # Grammar correction/sentence improvement
    "research",     # Requires deep research/analysis
    "planning",     # Complex task requiring step-by-step plan
    "creative",     # Creative writing/content generation
    "math",         # Mathematical calculations/problems
    "conversation"  # Casual conversation/chitchat
]
