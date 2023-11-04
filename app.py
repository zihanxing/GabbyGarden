import streamlit as st
import time
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from html_chatbot_template import css, bot_template, user_template
from src.sound import sound
from settings import IMAGE_DIR, DURATION, WAVE_OUTPUT_FILE


def extract_text(pdf_files):
    """
    Function to extract the text from a PDF file

    Args:
        pdf_file (file): The PDF files to extract the text from

    Returns:
        text (str): The extracted text from the PDF file
    """

    # Initialize the raw text variable
    text = ""

    # Iterate over the documents
    for pdf_file in pdf_files:
        print("[INFO] Extracting text from {}".format(pdf_file.name))

        # Read the PDF file
        pdf_reader = PdfReader(pdf_file)

        # Extract the text from the PDF pages and add it to the raw text variable
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text

def get_chunks(text):
    """
    Function to get the chunks of text from the raw text

    Args:
        text (str): The raw text from the PDF file

    Returns:
        chunks (list): The list of chunks of text
    """

    # Initialize the text splitter
    splitter = CharacterTextSplitter(
        separator="\n", # Split the text by new line
        chunk_size=1000, # Split the text into chunks of 1000 characters
        chunk_overlap=200, # Overlap the chunks by 200 characters
        length_function=len # Use the length function to get the length of the text
    )

    # Get the chunks of text
    chunks = splitter.split_text(text)

    return chunks

def get_vectorstore(chunks):
    """
    Function to create avector store for the chunks of text to store the embeddings

    Args:
        chunks (list): The list of chunks of text

    Returns:
        vector_store (FAISS): The vector store for the chunks of text
    """

    # Initialize the embeddings model to get the embeddings for the chunks of text
    embeddings = OpenAIEmbeddings()

    # Create a vector store for the chunks of text embeddings
    # Can use any other online vector store (Elasticsearch, PineCone, etc.)
    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vector_store

def get_conversation_chain(vector_store):
    """
    Function to create a conversation chain for the chat model

    Args:
        vector_store (FAISS): The vector store for the chunks of text
    
    Returns:
        conversation_chain (ConversationRetrievalChain): The conversation chain for the chat model
    """
    
    # Initialize the chat model using Langchain OpenAi API
    # Set the temperature and select the model to use
    # Can replace this with any other chat model (Llama, Falcom, etc.)
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.1)

    # Initialize the chat memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create a conversation chain for the chat model
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, # Chat model
        retriever=vector_store.as_retriever(), # Vector store
        memory=memory, # Chat memory
    )

    return conversation_chain

def generate_response(question):
    """
    Function to generate a response for the user query using the chat model

    Args:
        question (str): The user query

    Returns:
        response (str): The response from the chat model
    """

    # Get the response from the chat model for the user query
    response = st.session_state.conversations({'question': question})

    # Update the chat history
    st.session_state.chat_history = response['chat_history']

    # Add the response to the UI
    for i, message in enumerate(st.session_state.chat_history):
        # Check if the message is from the user or the chatbot
        if i % 2 == 0:
            # User message
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            # Chatbot message
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


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
    st.set_page_config(page_title="ChildPal", page_icon="🤖", layout="wide")

    # Add the custom CSS to the UI
    st.write(css, unsafe_allow_html=True)

    # Initialize the session state variables to store the conversations and chat history
    if "conversations" not in st.session_state:
        st.session_state.conversations = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # Set the page title
    st.header("Ask any questions you want~")

    # Input text box for user query
    # user_question = st.text_input("Upload your data and ask me anything?")
    # Ask me
    # Check if the user has entered a query/prompt
    # if user_question:
    #     # Call the function to generate the response
    #     generate_response(user_question)
    st.button("Ask me.")
    
    option = st.selectbox(
        "what is your favorite color?",
        ("Blue", "Red", "Green")
    )
    if option:
        st.write("Your favorite color is", option)
    
    st.code("""
        [theme]
        primaryColor="#F39C12"
        backgroundColor="#2E86C1"
        secondaryBackgroundColor="#AED6F1"
        textColor="#FFFFFF"
        font="monospace"
        """)

    number = st.sidebar.slider('Select a number:', 0, 10, 5)
    st.write('Selected number from slider widget is:', number)
    
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1)
    # st.ballons()
    
    if st.button('Record'):
        with st.spinner(f'Recording for {DURATION} seconds ....'):
            sound.record()
        st.success("Recording completed")

    if st.button('Play'):
        # sound.play()
        try:
            audio_file = open(WAVE_OUTPUT_FILE, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
        except:
            st.write("Please record sound first")

    # Sidebar menu
    with st.sidebar:
        st.subheader("MyStories")

        # Document uploader
        pdf_files = st.file_uploader("Upload a document you want to chat with", type="pdf", key="upload", accept_multiple_files=True)

        # Process the document after the user clicks the button
        if st.button("Start Chatting ✨"):
            # Add a progress spinner
            with st.spinner("Processing"):
                # Convert the PDF to raw text
                raw_text = extract_text(pdf_files)
                
                # Get the chunks of text
                chunks = get_chunks(raw_text)
                
                # Create a vector store for the chunks of text
                vector_store = get_vectorstore(chunks)

                # Create a conversation chain for the chat model
                st.session_state.conversations = get_conversation_chain(vector_store)

# Application entry point
if __name__ == "__main__":
    # Run the UI
    run_UI()