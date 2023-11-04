import streamlit as st
import os
import time
from PIL import Image
from html_chatbot_template import img_template
import streamlit.components.v1 as components
import io
import requests
import base64

API_TOKEN="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"
API_URL = "https://api-inference.huggingface.co/models/nerijs/pixel-art-xl"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
  response = requests.post(API_URL, headers=headers, json=payload)
  return response.content
image_bytes = query({
  "inputs": "Astronaut riding a tiger",
})
image_bytes_2 = query({
  "inputs": "Astronaut riding a horse",
})
image_bytes_3 = query({
  "inputs": "Astronaut riding a rabbit",
})
# You can access the image with PIL.Image for example
images=[]
images.append(Image.open(io.BytesIO(image_bytes)))
images.append(Image.open(io.BytesIO(image_bytes_2)))
images.append(Image.open(io.BytesIO(image_bytes_3)))

# img_byte_arr = io.BytesIO() 
# image.save(img_byte_arr, format='JPEG') # 或者使用 PNG 等其他格式 
# img_byte_arr = img_byte_arr.getvalue() # 将Byte流编码为base64字符串 
# img_base64 = base64.b64encode(img_byte_arr).decode()

import streamlit as st
import streamlit.components.v1 as components

_CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

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

    <div class="mySlides fade">
    <div class="numbertext">1 / 3</div>
    <img src="app/static/pic1.jpeg" style="width:100%">
    <div class="text">Caption Text</div>
    </div>

    <div class="mySlides fade">
    <div class="numbertext">2 / 3</div>
    <img src="app/static/pic2.jpg" style="width:100%">
    <div class="text">Caption Two</div>
    </div>

    <div class="mySlides fade">
    <div class="numbertext">3 / 3</div>
    <img src="app/static/pic3.jpg" style="width:100%">
    <div class="text">Caption Three</div>
    </div>

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
        
        
# tell_story()
# pic_transit()