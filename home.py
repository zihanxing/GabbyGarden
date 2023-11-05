import streamlit as st
import time
from dotenv import load_dotenv
from html_chatbot_template import css, bot_template, user_template

## Landing page UI
def run_UI():
    """
    The main UI function to display the UI for the webapp

    Args:
        None

    Returns:
        None
    """

    # Load the environment variables (API keys)
    load_dotenv()

    # Set the page tab title
    st.set_page_config(page_title="ChildPal", page_icon="🌼", layout="wide")

    # Add the custom CSS to the UI
    st.write(css, unsafe_allow_html=True)

    # Initialize the session state variables to store the conversations and chat history
    if "conversations" not in st.session_state:
        st.session_state.conversations = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Set the page title
    st.header("GabbyGarden 🌱\n \
        Sowing Seeds of Knowledge and Imagination for Kids 💫")
    
    # Sidebar menu
    with st.sidebar:
        st.subheader("About the app")

# Application entry point
if __name__ == "__main__":
    # Run the UI
    run_UI()
    