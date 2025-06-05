from langchain import ChatGroq
from config.settings import GROQ_API_KEY, LLM_MODEL, LLM_TEMPERATURE, get_full_model_name

def get_llm(model=None, temperature=None):
    """Initialize and return a ChatGroq model instance.
    Args:
        model (str, optional): The model name to use. Defaults to LLM_MODEL.
        temperature (float, optional): The temperature for the model. Defaults to LLM_TEMPERATURE.
    Returns:
        An initialized Groq LLM model.
    """
    model = model or LLM_MODEL
    temperature = temperature if temperature is not None else LLM_TEMPERATURE

    full_model_name = get_full_model_name(model)

    return ChatGroq(
        model=full_model_name,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )