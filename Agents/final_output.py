from typing import Dict, Any

def prepare_final_output(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepares the final output to present to the user.

    Args:
        state: The current workflow state.

    Returns:
        Updated state with the finalized output.
    """
    language = state.get("language", "python")
    
    if "code_output" in state:
        format_code = f"```{language}\n{state['code_output']}\n```"
        output = f"Here's the {language} code for your requested:\n\n{format_code}"
    else:
        output = "I couldn't process your request. Please try rephrasing your question."
        
    return {
        **state,
        "output": output,
    }
        