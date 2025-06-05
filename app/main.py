import streamlit as st
from agents.user_input import process_user_input
from core.graph import build_workflow_graph
from config.settings import APP_TITLE, APP_DESCRIPTION, APP_VERSION, GROQ_MODEL, get_full_model_name
import os

def initialize_sesion_state():
    """Initialize the session state for the application."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "workflow" not in st.session_state:
        st.session_state.workflow = build_workflow_graph()
    
def display_chat_history():
    """Display the chat history in the Streamlit interface."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    """Main entry point for the Streamlit application."""
    
    initialize_sesion_state()
    
    st.set_page_config(page_title=APP_TITLE, page_icon=":robot:")
    st.title(f"{APP_TITLE}")
    st.caption(f"Version: {APP_VERSION}")
    st.markdown(APP_DESCRIPTION)
    
    with st.sidebar:
        st.header("Model Settings")
       
        groq_model = list(GROQ_MODEL) + list(GROQ_MODEL.values())
        selected_model = st.selectbox(
            "Groq Model",
            options=groq_model,
            index=groq_model.index("llama3-70b") if "llama3-70b" in groq_model else 0
        )
        
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
        
        if st.button("Apply Settings"):
            os.environ["LLM_MODEL"] = get_full_model_name(selected_model)
            os.environ["LLM_TEMPERATURE"] = str(temperature)
            st.success(f"Settings applied: {get_full_model_name(selected_model)} / temp= {temperature}")
            
            st.session_state.workflow = build_workflow_graph()
    
    st.markdown("---")
    display_chat_history()
    if prompt := st.chat_input("What would you like help with? (e.g., 'Generate a Python function to sort a list')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat.mesage("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            initial_state = process_user_input(prompt)
            with st.spinner("Processing your request..."):
                result = st.session_state.workflow.invoke(initial_state)
            message_placeholder.markdown(result["output"])
        st.session_state.messages.append({"role": "assistant", "content": result["output"]})
        
if __name__ == "__main__":
    main()
        
       
       