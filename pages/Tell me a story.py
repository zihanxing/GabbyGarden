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

def tell_story():
    img_path = "assets/pics/"
    st.audio("assets/example.mp3", format='audio/mp3')
    
    for image in images: 
        st.image(image, use_column_width='auto') 
        time.sleep(10) # 间隔2秒显示下一张图片 
            # st.experimental_rerun() # 重运行脚本以更新图片显示
    # for filename in os.listdir(img_path):
    #     # img = Image.open(img_path+filename)
    #     time.sleep(2)
    #     # st.markdown(f"<img src='{'../'+img_path+filename}'>", unsafe_allow_html=True)
    #     # <img src="assets/pics/pic1.jpeg" style="text-align: center;">
    #     st.image(img_path+filename, width=600)  
    #     st.experimental_rerun()  

tell_story()