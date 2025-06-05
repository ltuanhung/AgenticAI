import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

LLM_MODEL = os.getenv("LLM_MODEL", "llama-3-70b-8192")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))

GROQ_MODEL = {
    "llama-3-8b": "llama-3-8b-8192",
    "llama-3-70b": "llama-3-70b-8192",
    "mixtral-8x7b": "mixtral-8x7b-32768",
    "gemma-7b": "gemma-7b-it",
}

def get_full_model_name(model_name):
   return GROQ_MODEL.get(model_name, model_name)

APP_TITLE = "Quan-Agentic AI"
APP_DESCRIPTION = "AI Agent system that helps you write, review, understand, and testcase."
APP_VERSION = "1.0.0 (MVP)"
DEBUG = os.getenv("DEBUG_MODE", "False").lower() == "true"