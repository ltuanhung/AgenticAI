from typing import Dict, Any
from core.llm import get_llm
from langchain.prompts import ChatPromptTemplate

def generate_code(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates code based on the user's query.

    Args:
        state: The curent workflow state.

    Returns:
       updated state with the generated code.
    """
    llm = get_llm()
    
    language = state.get("language", "python")
    
    code_prompt = ChatPromptTemplate.from_template("""
    You are an expert programmer with extensive knowledge of programming languages, algorithms, and best practices.
    
    User Request: {query}
    
    Please write code in {language} that fulfills this request. Follow these guidelines:
    1. Use appropriate and morden {language} practices and idioms.
    2. Include helfful comments explaining yout approach.
    3. Handle edge cases and potiential errors gracefully.
    4. Organize the code logically and make it readable.
    5. Use appropriate variable name and codeing conventions for {language}.
    CODE:
    """)
    
    chain = code_prompt | llm;
    
    generate_code = chain.invoke({("query"): state["query"], "language": language}).content
    
    history = state.get("history", [])
    history.append({"role": "code_agent", "content": "generated_code"})
    
    return {
        **state,
        "code_output": generate_code,
        "history": history,
    }