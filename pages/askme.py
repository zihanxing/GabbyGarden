import streamlit as st
from streamlit_mic_recorder import mic_recorder,speech_to_text
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_chatbot_template import css, bot_template, user_template
import openai


def generate_response(question):
    """
    Function to generate a response for the user query using the chat model

    Args:
        question (str): The user query

    Returns:
        response (str): The response from the chat model
    """

    # Get the response from the chat model for the user query
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant","content": "Ask me any questions."}]
    if "chat_hist" not in st.session_state:
        st.session_state["chat_hist"] = ["Ask me any questions."]
    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])
        
    if question:
        # message
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.chat_hist.append(question)
        # st.chat_message("user").write(question)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
    
        st.session_state.chat_hist.append(msg.content)
        # st.chat_message("assistant").write(msg.content)
        # st.write(st.session_state.messages)
        st.write(st.session_state.chat_hist)
        # Add the response to the UI
        for i, message in enumerate(st.session_state.chat_hist):
            # Check if the message is from the user or the chatbot
            if i % 2 == 0:
                # User message
                st.write(bot_template.replace(
                    "{{MSG}}", message), unsafe_allow_html=True)
            else:
                # Chatbot message
                st.write(user_template.replace(
                    "{{MSG}}", message), unsafe_allow_html=True)
            
def mic():
    state=st.session_state

    if 'text_received' not in state:
        state.text_received=[]

    c1=st.columns(1)
    # st.write("Convert speech to text:")
    text=speech_to_text(language='en',start_prompt="Ask Me 😊",
                        use_container_width=True,just_once=True,key='STT')

    if text:       
        state.text_received.append(text)
        # st.session_state.conversations = get_conversation_chain(text)
        generate_response(text)

    # for text in state.text_received:
    #     st.text(text)


mic()