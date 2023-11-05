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
        i+=1
    return slides_html

def display_tell_story(chunk_prompt):
    images=[]
    chunk=[]
    for item in chunk_prompt:
        temp_query=query({"inputs":item[1]})
        images.append(Image.open(io.BytesIO(temp_query)))
        chunk.append(item[0])
    image_bytes = query({
      "inputs": "Create a digital image of a child making a colorful greeting card for his best friend, filled with drawings of their favorite shared activities. Keep the style simple and cartoon-like for kids.",
    })
    image_bytes_2 = query({
      "inputs": "Create a colorful, cartoon-style image of a small child cheerfully helping with chores around the house, such as picking up toys and setting the table.",
    })
    image_bytes_3 = query({
      "inputs": "Create a pixel art image of a child presenting a handmade gift to their father, using bright and simple flat colors. The father should look happy and the gift can be something like a drawing or a crafted item.",
    })
    # You can access the image with PIL.Image for example
    images=[]
    images.append(Image.open(io.BytesIO(image_bytes)))
    images.append(Image.open(io.BytesIO(image_bytes_2)))
    images.append(Image.open(io.BytesIO(image_bytes_3)))
    image_base64=pil_to_image(images)
    slides_html=generate_slides_html(image_base64)

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

        <div style="text-align:center">
        <span class="dot"></span> 
        <span class="dot"></span> 
        <span class="dot"></span> 
        </div>

        <script>
        let slideIndex = 0;
        showSlides();

        function showSlides() {{
        let i;
        let slides = document.getElementsByClassName("mySlides");
        let dots = document.getElementsByClassName("dot");
        for (i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";  
        }}
        slideIndex++;
        if (slideIndex > slides.length) {{slideIndex = 1}}    
        for (i = 0; i < dots.length; i++) {{
            dots[i].className = dots[i].className.replace(" active", "");
        }}
        slides[slideIndex-1].style.display = "block";  
        dots[slideIndex-1].className += " active";
        setTimeout(showSlides, 5000); // Change image every 5 seconds
        }}
        </script>
        </body>
        </html> 

            """,
        height=600,
    )

def tell_story():
    img_path = "assets/pics/"
    st.audio("assets/example.mp3", format='audio/mp3')
    
# def pic_transit():
#     for image in images: 
#         st.session_state.img = image
#         st.image(image, use_column_width='auto') 
#         time.sleep(10) 

# 初始设置session_state的键，如果不存在
if 'show_html' not in st.session_state:
    st.session_state.show_html = False

# 如果按钮被按下，切换状态
col1, col2 = st.columns(2)
with col1:
    if st.button('Switch to HTML UI'):
        st.session_state.show_html = True
with col2:
    if st.button('Switch to Conversation UI'):
        st.session_state.show_html = False

# 根据session_state的状态显示不同的内容
if not st.session_state.show_html:
    # 显示HTML UI
    display_tell_story(chunk_prompt)
else:
    # 显示对话式UI
    # question = know()
    question = "what kind of animal do you like?"
    st.write(question)
    ans = speech_to_text(language='en',start_prompt="Let me know YOU 😊",
                        use_container_width=True,just_once=True,key='STT')
    if ans:
        st.write(ans)
    # re = generate_story(mic())
# 其他Streamlit内容
# ...


     

# tell_story()
# pic_transit()


# date=datetime.now()
# ymd=date.strftime("%Y-%m-%d")
# formatted_time = ymd+"-"+date.strftime("%H-%M-%S")
# # 定义文件夹的名字
# folder_name = f"static/{formatted_time}"

# # 使用os模块的mkdir函数创建文件夹
# try:
#     os.mkdir(folder_name)
#     print(f"Folder '{folder_name}' created successfully.")
# except FileExistsError:
#     print(f"Folder '{folder_name}' already exists.")

# for img in images:
#     date=datetime.now()
#     ymd=date.strftime("%Y-%m-%d")
#     formatted_time = ymd+"-"+date.strftime("%H-%M-%S")  
    
#     img.save(f'{folder_name}/{formatted_time}.jpg', 'JPEG')


# # Function to generate the HTML for the image slides
# def generate_slides_html_2(image_folder):
#     images = os.listdir(image_folder)
#     slides_html = ""
#     for i,image in enumerate(images):
        
        
#         slide = f"""
#         <div class="mySlides fade">
#             <div class="numbertext">{i + 1} / {len(images)}</div>
#             <img src="app/static/{image}" style="width:100%">
#             <div class="text">Caption for </div>
#         </div>
#         """
#         slides_html += slide
#     return slides_html

# Directory where your images are stored
# image_folder = "static"
# image_folder=pil_to_image(images)
# images = os.listdir(image_folder)
# Call the function to generate the HTML for the slides
# slides_html = generate_slides_html_2(folder_name)