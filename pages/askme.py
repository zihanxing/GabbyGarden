import streamlit as st
from streamlit_mic_recorder import speech_to_text
from dotenv import load_dotenv
from html_chatbot_template import css, bot_template, user_template
from APIs.talk import chat_with_child
from APIs.text2speech import get_speech_from_text
from pages.helper import autoplay_audio

def generate_response(conversation_log):
    """
    Function to generate a response for the user query using the chat model

    Args:
        question (str): The user query

    Returns:
        response (str): The response from the chat model
    """

    # Get the response from the chat model for the user query
    if "system" not in st.session_state:
        st.session_state["system"] = 0
    if "chat_hist" not in st.session_state:
        st.session_state["chat_hist"] = []
    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])
        
    st.session_state.chat_hist.extend(conversation_log)
    st.write(css, unsafe_allow_html=True)
    welcome = "Hello! Welcome to GabbyGarden! I am Gab.\n You can ask me any question you like! I'm here to help you learn and understand new things."
    # st.write(st.session_state.chat_hist)
    for message in st.session_state.chat_hist:
        # Check if the message is from the user or the chatbot
        if message['role'] == 'assistant':
            # bot message
            st.write(bot_template.replace(
                "{{MSG}}", message['content']), unsafe_allow_html=True)
        elif message['role'] == 'system' and st.session_state.system==0:
            st.session_state.system = 1
            st.write(bot_template.replace(
                "{{MSG}}", welcome), unsafe_allow_html=True)
        elif message['role'] == 'user':
            # user message
            st.write(user_template.replace(
                "{{MSG}}", message['content']), unsafe_allow_html=True)
    autoplay_audio("./assets/text2speech.mp3")  
                
def mic():
    state=st.session_state

    if 'text_received' not in state:
        state.text_received=[]
    # if '_last_audio_id' not in state:
    #     state._last_audio_id = 0

    c1=st.columns(1)
    # st.write("Convert speech to text:")
    text=speech_to_text(language='en',start_prompt="Ask Me 😊",
                        use_container_width=True,just_once=True,key='STT')
    
    if text:       
        state.text_received.append(text)
        # st.session_state.conversations = get_conversation_chain(text)
        log = chat_with_child(text)
        # st.markdown(log)
        generate_response(log)
        # autoplay_audio("./assets/speech.mp3")   

mic()