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
    st.markdown("""
                <style>
                    /* Center the container horizontally */
                    .image-container {
                        display: flex;
                        justify-content: center; /* Center horizontally */
                    }
                    
                    /* Style the images (optional) */
                    .image-container img {
                        width: 350px; /* Set the width of each image */
                        height: auto; /* Maintain the aspect ratio */
                        margin-top: 30px 
                    }
                </style>
                <div class="image-container">
                    <img src="app/static/flowers.GIF" width="300" height="200"/>
                </div>
                """, unsafe_allow_html=True)
    
    # Sidebar menu
    with st.sidebar:
        st.subheader("About the app")
        st.markdown("""
                    With **GabbyGarden AI**, kids can just 
                    - speak up and listen to stories, 
                    - making it easy for them to learn and have fun.
                    It's like having a smart friend 😆 who's always there to explore and learn with them👏🏻👏🏼👏🏼👏🏽👏🏾.
                    """)

# Application entry point
if __name__ == "__main__":
    # Run the UI
    run_UI()
    