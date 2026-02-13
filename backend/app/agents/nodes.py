import os
from typing import Dict, Any
from openai import OpenAI
from .state import AgentState

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(system_prompt: str, user_message: str, model: str = "gpt-4o-mini", temperature: float = 0.7) -> str:
    """Helper function to call OpenAI API."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# ============== ROUTER/DECISION AGENT ==============
def router_agent(state: AgentState) -> AgentState:
    """
    Decision Agent: Analyzes the query and determines which specialized agent should handle it.
    """
    system_prompt = """You are a query classifier. Analyze the user's query and classify it into exactly ONE of these categories:

- general: General knowledge questions, facts, explanations
- coding: Programming, code writing, debugging, technical implementation
- grammar: Grammar correction, sentence improvement, rephrasing
- research: Questions requiring deep analysis, comparisons, or detailed research
- planning: Complex tasks needing step-by-step breakdown or project planning
- creative: Creative writing, storytelling, content generation
- math: Mathematical problems, calculations, equations
- conversation: Casual chat, greetings, small talk

Respond with ONLY the category name, nothing else."""

    query_type = call_llm(system_prompt, state["query"], temperature=0).strip().lower()

    # Validate the response
    valid_types = ["general", "coding", "grammar", "research", "planning", "creative", "math", "conversation"]
    if query_type not in valid_types:
        query_type = "general"

    state["query_type"] = query_type
    state["selected_agent"] = query_type

    return state


# ============== GENERAL QA AGENT ==============
def general_agent(state: AgentState) -> AgentState:
    """
    General Agent: Handles general knowledge questions and explanations.
    """
    system_prompt = """You are a knowledgeable assistant. Provide clear, accurate, and helpful answers to questions.
Be concise but comprehensive. Use examples when helpful.
If you're not sure about something, say so."""

    context = state.get("research_context", "")
    query = state["query"]

    if context:
        query = f"Context: {context}\n\nQuestion: {query}"

    response = call_llm(system_prompt, query)
    state["response"] = response

    return state


# ============== CODING AGENT ==============
def coding_agent(state: AgentState) -> AgentState:
    """
    Coding Agent: Handles programming and code-related questions.
    """
    system_prompt = """You are an expert programmer and software engineer. Help with:
- Writing clean, efficient code
- Debugging and fixing issues
- Explaining programming concepts
- Code reviews and improvements
- Best practices and design patterns

When providing code:
1. Use proper formatting with code blocks
2. Add helpful comments
3. Explain the logic
4. Consider edge cases
5. Follow best practices for the language"""

    response = call_llm(system_prompt, state["query"])
    state["response"] = response

    return state


# ============== GRAMMAR AGENT ==============
def grammar_agent(state: AgentState) -> AgentState:
    """
    Grammar Agent: Handles grammar correction and sentence improvement.
    """
    system_prompt = """You are an expert editor and grammar specialist. Your tasks:
1. Correct any grammatical errors
2. Improve sentence structure and clarity
3. Enhance word choice while maintaining the original meaning
4. Make the text more professional/natural as appropriate

Format your response as:
**Corrected:** [The corrected text]

**Changes made:**
- [List each change and why]

If the text is already correct, say so and optionally suggest stylistic improvements."""

    response = call_llm(system_prompt, state["query"])
    state["response"] = response

    return state


# ============== RESEARCH AGENT ==============
def research_agent(state: AgentState) -> AgentState:
    """
    Research Agent: Handles questions requiring deep analysis and research.
    """
    system_prompt = """You are a thorough researcher and analyst. For research questions:

1. Break down the topic into key aspects
2. Provide comprehensive analysis
3. Consider multiple perspectives
4. Cite general knowledge and reasoning
5. Identify areas of uncertainty
6. Summarize key findings

Structure your response clearly with headings if the topic is complex."""

    # First, gather context through analysis
    analysis_prompt = """Analyze this query and identify:
1. Key concepts to explore
2. Important aspects to cover
3. Potential sub-questions to answer

Query: """ + state["query"]

    context = call_llm(
        "You are a research assistant. Identify key aspects to research.",
        analysis_prompt,
        temperature=0.3
    )
    state["research_context"] = context

    # Then provide comprehensive response
    full_query = f"""Research context and aspects to cover:
{context}

User's question: {state["query"]}

Provide a comprehensive, well-researched response."""

    response = call_llm(system_prompt, full_query)
    state["response"] = response

    return state


# ============== PLANNER AGENT ==============
def planner_agent(state: AgentState) -> AgentState:
    """
    Planner Agent: Creates step-by-step plans for complex tasks.
    """
    system_prompt = """You are a strategic planner and project manager. For complex tasks:

1. Understand the goal clearly
2. Break it down into manageable steps
3. Identify dependencies between steps
4. Estimate complexity/effort for each step
5. Suggest tools or resources needed
6. Anticipate potential challenges

Format your response as a clear, actionable plan with numbered steps.
Include timeline suggestions if relevant."""

    # First create a plan
    plan_prompt = f"""Create a detailed plan for: {state["query"]}

List the steps needed to accomplish this task."""

    plan_response = call_llm(
        "You are a planning assistant. Create clear, actionable plans.",
        plan_prompt,
        temperature=0.3
    )

    # Parse steps (simple extraction)
    steps = [line.strip() for line in plan_response.split('\n') if line.strip()]
    state["plan"] = steps

    # Provide full response with plan
    response = call_llm(system_prompt, state["query"])
    state["response"] = response

    return state


# ============== CREATIVE AGENT ==============
def creative_agent(state: AgentState) -> AgentState:
    """
    Creative Agent: Handles creative writing and content generation.
    """
    system_prompt = """You are a creative writer with expertise in various styles and formats.
You can help with:
- Creative writing (stories, poems, scripts)
- Content creation (blog posts, social media)
- Brainstorming ideas
- Developing characters and narratives
- Writing in specific tones or styles

Be imaginative, engaging, and adapt to the user's creative vision."""

    response = call_llm(system_prompt, state["query"], temperature=0.9)
    state["response"] = response

    return state


# ============== MATH AGENT ==============
def math_agent(state: AgentState) -> AgentState:
    """
    Math Agent: Handles mathematical problems and calculations.
    """
    system_prompt = """You are a mathematics expert. Help with:
- Solving equations and problems
- Explaining mathematical concepts
- Step-by-step solutions
- Proofs and derivations
- Applied mathematics

Always show your work step-by-step.
Use clear mathematical notation.
Verify your answers when possible."""

    response = call_llm(system_prompt, state["query"], temperature=0.2)
    state["response"] = response

    return state


# ============== CONVERSATION AGENT ==============
def conversation_agent(state: AgentState) -> AgentState:
    """
    Conversation Agent: Handles casual conversation and chitchat.
    """
    system_prompt = """You are a friendly conversational assistant.
Be warm, engaging, and natural in your responses.
Keep responses concise for casual conversation.
Show personality while being helpful."""

    response = call_llm(system_prompt, state["query"], temperature=0.8)
    state["response"] = response

    return state


# ============== RESPONSE ENHANCER ==============
def response_enhancer(state: AgentState) -> AgentState:
    """
    Enhances the final response for clarity and completeness.
    """
    if state.get("error"):
        state["response"] = f"I apologize, but I encountered an issue: {state['error']}"
        return state

    if not state.get("response"):
        state["response"] = "I apologize, but I couldn't generate a response. Please try again."

    return state
