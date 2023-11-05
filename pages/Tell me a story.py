import streamlit as st
import os
import time
from PIL import Image
from html_chatbot_template import img_template
import streamlit.components.v1 as components
import io
import requests
import base64
from datetime import datetime
from pages.askme import mic
from streamlit_mic_recorder import speech_to_text
from APIs.storyteller import ask_question, story_trunks
from APIs.helper import autoplay_audio
from APIs.text2speech import get_speech_from_text
import json

# _CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/nerijs/pixel-art-xl"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.content

def pil_to_image(images):
    image_base64=[]
    for img in images:
        img_byte_arr = io.BytesIO() 
        img.save(img_byte_arr, format='PNG') # 或者使用 PNG 等其他格式 
        img_byte_arr = img_byte_arr.getvalue() # 将Byte流编码为base64字符串 
        img_base64 = base64.b64encode(img_byte_arr).decode()
        image_base64.append(img_base64)
    return image_base64


# Function to generate the HTML for the image slides
def generate_slides_html(base64_string_image_folder):
    # images = os.listdir(image_folder)
    slides_html = ""
    i=0
    for base64_string in base64_string_image_folder:
        
        slide = f"""
        <div class="mySlides fade">
            <div class="numbertext">{i + 1} / {len(base64_string_image_folder)}</div>
            <img src="data:image/jpeg;base64,{base64_string}" style="width: 600px; height: 600px;">
            <div class="text">Caption for </div>
        </div>
        """
        slides_html += slide
        # print(f"iiiii:{i}")
        # i+=1
    return slides_html

def display_tell_story(chunk_prompt):
    images=[]
    chunk=[]
    
    progress_text = "Generating the Story 💨"
    my_bar = st.progress(0, text=progress_text)

    for i, item in enumerate(chunk_prompt):
        my_bar.progress(int((i+1)/len(chunk_prompt)*100), text=progress_text)
    # for item in chunk_prompt:
        temp_query=query({"inputs":item[1]})
        images.append(Image.open(io.BytesIO(temp_query)))
        chunk.append(item[0])

    image_base64=pil_to_image(images)
    slides_html=generate_slides_html(image_base64)
    print(f"image_base64:{len(image_base64)}")
    
    story = " ".join(chunk)
    duration = {}
    for i, text in enumerate(chunk):
        duration[i] = len(text.split(" "))/30*12000

    print(f"Duration: {duration}, Type: {type(duration)}")
    duration = json.dumps(duration)
    print(f"Duration: {duration}, Type: {type(duration)}")
    
    get_speech_from_text(story ,'story')
    autoplay_audio('./assets/story.mp3')
    
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
        * {{box-sizing: border-box;}}
        body {{font-family: Verdana, sans-serif;}}
        .mySlides {{display: none;}}
        img {{vertical-align: middle;}}

        /* Slideshow container */
        .slideshow-container {{
        max-width: 1000px;
        position: relative;
        margin: auto;
        }}

        /* Caption text */
        .text {{
        color: #f2f2f2;
        font-size: 15px;
        padding: 8px 12px;
        position: absolute;
        bottom: 8px;
        width: 100%;
        text-align: center;
        }}

        /* Number text (1/3 etc) */
        .numbertext {{
        color: #f2f2f2;
        font-size: 12px;
        padding: 8px 12px;
        position: absolute;
        top: 0;
        }}

        /* The dots/bullets/indicators */
        .dot {{
        height: 15px;
        width: 15px;
        margin: 0 2px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.6s ease;
        }}

        .active {{
        background-color: #717171;
        }}

        /* Fading animation */
        .fade {{
        animation-name: fade;
        animation-duration: 1.5s;
        }}

        @keyframes fade {{
        from {{opacity: .4}} 
        to {{opacity: 1}}
        }}

        /* On smaller screens, decrease text size */
        @media only screen and (max-width: 300px) {{
        .text {{font-size: 11px}}
        }}
        </style>
        </head>
        <body>

        <h2>Automatic Slideshow</h2>

        <div class="slideshow-container"> 
            {slides_html}
        </div>
        <br>

        <script>
        let slideIndex = 0;
        var duration = { duration };
        console.log(duration['0']);
        console.log(duration[1]);
        console.log(duration[2]);
        
        showSlides();
        
        function showSlides() {{
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");
        for (i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";  
        }}
        slideIndex++;

        slides[slideIndex-1].style.display = "block";  

        setTimeout(showSlides, duration[slideIndex-1]); // Change image every 5 seconds
        }}
        </script>
        </body>
        </html> 

            """,
        height=600,
    )
    # get_speech_from_text(chunk[0], f'strory_{0}')
    # autoplay_audio(f'./assets/strory_{0}.mp3')

def tell_story():
    img_path = "assets/pics/"
    st.audio("assets/example.mp3", format='audio/mp3')


# 初始设置session_state的键，如果不存在
if 'show_html' not in st.session_state:
    st.session_state.show_html = False
if 'ans' not in st.session_state:
    st.session_state.ans = ""
if 'question' not in st.session_state:
    st.session_state.question = ""
if 'log' not in st.session_state:
    st.session_state.log = []

# 如果按钮被按下，切换状态
col1, col2 = st.columns(2)
with col1:
    if st.button('Listen To A Story 📖'):
        st.session_state.show_html = True
with col2:
    if st.button("Do it Again 🔄"):
        st.session_state.show_html = False
        
# 根据session_state的状态显示不同的内容
if  st.session_state.show_html:
    # 显示HTML UI
    with st.spinner('Generating Prompts...💪🏻'):
        time.sleep(5)
        chunk_prompt = story_trunks(st.session_state.question, 
                                    st.session_state.ans,
                                    st.session_state.log)
    # st.write(chunk_prompt)
    display_tell_story(chunk_prompt)
    # st.ballons()
else:
    # 显示对话式UI
    st.session_state.question, st.session_state.log = ask_question()
    st.write(st.session_state.question)
    ans = speech_to_text(language='en',start_prompt="Let me know YOU 😊",
                        use_container_width=True,just_once=True,key='ANS')
        
    if ans:
        st.session_state.ans = ans
        st.write("Now Let's Listen to a Story 🥳")


     

# tell_story()
# pic_transit()

