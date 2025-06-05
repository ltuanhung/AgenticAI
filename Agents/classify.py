from typing import Any, Dict
from core.llm import get_llm
from langchain.prompts import ChatPromptTemplate

def classify_question(state: Dict[str, Any]) -> Dict[str, Any]:
    """ Classify the user's question to determine the appropriate processing path.
    
    Args:
        state: The current state of the workflow.
        
    Returns:
        Updated state with the classification information.
    """
    llm = get_llm()
    classification_prompt = ChatPromptTemplate.from_template("""
    You are an AI that classifies progamming questions into specific categories.
    
    Please classify the following query into one of these categories:
    -code_generation: User wants you to generate code.
    -code_explanation: User wants an explanation code.
    -error_fixing: User wants you to fix an error in code.
    -general_programming: General programming concepts or questions.
    -github_repo: User wants to analyze a GitHub repository.
    
    Also, determine the programming language the user is interested in (python, javascript, etc.).
    If not specified, assume the most appropriate language for the task.
    User Query: {query}
    
    Provide your answer in this format:
    Category: [category name]
    Language: [language name]
    """)
    
    chain = classification_prompt | llm
    
    result = chain.invoke({("query"): state["query"]}).content
    
    category = "code"
    language = "python"
    
    if "Category:" in result:
        category_line = result.split("Category:")[1].split("\n")[0].strip().lower()
        category_map = {
            "code_generation": "code",
            "code_explanation": "doc",
            "error_fixing": "code",
            "general_programming": "doc",
            "github_repo": "github"
        }
        if category_line in category_map:
            category = category_map[category_line]
    
    if "Language:" in result:
        language_line = result.split("Language:")[1].split("\n")[0].strip().lower()
    
    history = state.get("history", [])
    history.append({"role": "classify_agent", "content": f"Classofycation: {category}, Language: {language}"})
    
    return {
        **state,
        "category": category,
        "language": language,
        "classification": result,
        "history": history,
    }
