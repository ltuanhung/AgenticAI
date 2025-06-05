from typing import Dict, Any, TypedDict, Optional, List
from langgraph.graph import StateGraph
from agents.classify import classify_question
from agents.code_agent import generate_code
from agents.final_output import prepare_final_output

class AgentState(TypedDict):
    """Defines the state structure for the agent workflow."""
    query: str
    category: Optional[str]
    language: Optional[str]
    history: List[Dict[str, str]]
    classification_detail: Optional[str]
    code_output: Optional[str]
    output: Optional[str]
    
def route_based_on_category(state: Dict[str, Any]) -> str:
    """Route to the appropriate agent based on the category.
    
    Args:
        state: The current state of the workflow.
    Returns:
        The name of the next node to execute.
    """
    return "code_agent"

def build_workflow_graph():
    """Builds the return the LangGraph workflow for handling user queries."""
    
    graph = StateGraph(AgentState)
    
    # Define the workflow nodes
    graph.add_node("classify", classify_question)
    graph.add_node("code_agent", generate_code)
    graph.add_node("final_output", prepare_final_output)
    
    # Define the transitions between nodes
    graph.add_transition("classify", route_based_on_category)
    graph.add_transition("code_agent", "final_output")
    
    graph.set_entry_point("classify")
    graph.set_exit_point("final_output")
    
    workflow = graph.compile();
    
    return workflow
 