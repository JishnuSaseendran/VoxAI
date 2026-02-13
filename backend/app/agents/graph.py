from typing import Dict, Any
from langgraph.graph import StateGraph, END

from .state import AgentState
from .nodes import (
    router_agent,
    general_agent,
    coding_agent,
    grammar_agent,
    research_agent,
    planner_agent,
    creative_agent,
    math_agent,
    conversation_agent,
    response_enhancer
)


def route_to_agent(state: AgentState) -> str:
    """
    Conditional edge function that routes to the appropriate agent based on query type.
    """
    agent_type = state.get("selected_agent", "general")

    routing_map = {
        "general": "general_agent",
        "coding": "coding_agent",
        "grammar": "grammar_agent",
        "research": "research_agent",
        "planning": "planner_agent",
        "creative": "creative_agent",
        "math": "math_agent",
        "conversation": "conversation_agent"
    }

    return routing_map.get(agent_type, "general_agent")


def create_agent_graph() -> StateGraph:
    """
    Creates the multi-agent graph using LangGraph.

    Graph structure:
    START -> router -> [agent based on classification] -> enhancer -> END
    """
    # Create the graph with our state schema
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("general_agent", general_agent)
    workflow.add_node("coding_agent", coding_agent)
    workflow.add_node("grammar_agent", grammar_agent)
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("planner_agent", planner_agent)
    workflow.add_node("creative_agent", creative_agent)
    workflow.add_node("math_agent", math_agent)
    workflow.add_node("conversation_agent", conversation_agent)
    workflow.add_node("enhancer", response_enhancer)

    # Set entry point
    workflow.set_entry_point("router")

    # Add conditional edges from router to specialized agents
    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "general_agent": "general_agent",
            "coding_agent": "coding_agent",
            "grammar_agent": "grammar_agent",
            "research_agent": "research_agent",
            "planner_agent": "planner_agent",
            "creative_agent": "creative_agent",
            "math_agent": "math_agent",
            "conversation_agent": "conversation_agent"
        }
    )

    # All agents connect to enhancer
    workflow.add_edge("general_agent", "enhancer")
    workflow.add_edge("coding_agent", "enhancer")
    workflow.add_edge("grammar_agent", "enhancer")
    workflow.add_edge("research_agent", "enhancer")
    workflow.add_edge("planner_agent", "enhancer")
    workflow.add_edge("creative_agent", "enhancer")
    workflow.add_edge("math_agent", "enhancer")
    workflow.add_edge("conversation_agent", "enhancer")

    # Enhancer goes to END
    workflow.add_edge("enhancer", END)

    # Compile the graph
    return workflow.compile()


# Create a singleton instance of the compiled graph
_agent_graph = None


def get_agent_graph():
    """Get or create the agent graph singleton."""
    global _agent_graph
    if _agent_graph is None:
        _agent_graph = create_agent_graph()
    return _agent_graph


def run_agent(query: str, history: list = None) -> Dict[str, Any]:
    """
    Run the multi-agent system on a query.

    Args:
        query: The user's question/request
        history: Optional conversation history

    Returns:
        Dict containing the response and metadata
    """
    if history is None:
        history = []

    # Initialize the state
    initial_state: AgentState = {
        "query": query,
        "query_type": None,
        "selected_agent": None,
        "plan": None,
        "research_context": None,
        "refined_query": None,
        "response": None,
        "history": history,
        "error": None
    }

    # Get the graph and run it
    graph = get_agent_graph()

    try:
        final_state = graph.invoke(initial_state)

        return {
            "response": final_state.get("response", "No response generated"),
            "query_type": final_state.get("query_type"),
            "agent_used": final_state.get("selected_agent"),
            "plan": final_state.get("plan"),
            "success": True
        }
    except Exception as e:
        return {
            "response": f"An error occurred: {str(e)}",
            "query_type": None,
            "agent_used": None,
            "plan": None,
            "success": False,
            "error": str(e)
        }
