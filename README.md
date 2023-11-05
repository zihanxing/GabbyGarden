# GabbyGarden 🌱

**Sowing Seeds of Knowledge and Imagination for Kids**

*Hackathon Project By Juan Peng, Haoyang Ma, Hongxuan(Leo) Li, Zihan(Zach) Xing*


## 😇 Inspiration 
We built GabbyGarden because we know kids are full of questions and love stories. Sometimes they ask things that even grown-ups don't know. We wanted to make sure they always have someone to talk to, who can answer their questions anytime. So, we made a friendly AI that can chat with them and tell them stories in a fun way. With GabbyGarden, kids can just speak up and listen to stories, making it easy for them to learn and have fun, even if they can't read or write yet. It's like having a smart friend who's always there to explore and learn with them.

## 🤖 What it does 
GabbyGarden is designed to be a child’s interactive companion that fosters learning and satisfies their curiosity. It does this by:

1. Answering Questions: Kids can ask any question, and our AI is built to provide answers that are easy for children to understand, helping them learn about the world around them.

2. Telling Stories: It uses voice and visuals to tell engaging stories, making storytime more dynamic and educational.

3. Supporting Learning: The tool is voice-activated, making it easy for kids who can't type or read fluently to interact with it and discover new things.

In short, GabbyGarden is an AI tool that makes learning interactive and fun for kids by answering their questions and telling stories in a way that captivates their imagination.

## 🛠️ How we built it 
For the Generative AI aspect of our project, we utilized some of the most cutting-edge models in the field together with their **APIs**. These included **GPT-3.5-turbo**, **GPT-4.0**, **StableDiffusion-XL-1.0**, and the **Pixel Art LoRA** model. In addition to this, we devoted considerable time to **Prompt Engineering** to ensure the optimal performance of our project.

We utilized **Streamlit** to develop an interface that is child-friendly. This approach ensures minimal effort is required from children in terms of inputting and reading. As a result, children can effortlessly receive informative answers and enjoy engaging stories complete with audio and visuals.

In addition to the above, we employed APIs from both **streamlit-mic-recorder** and **underthesea** to guarantee a seamless transition between text and speech. Meanwhile, **SQLite3** is employed for data storage, specifically for data that facilitates interaction with children.

## 🚧 Challenges we ran into
One key challenge was designing our AI to understand and respond appropriately to the diverse questions children might ask, requiring us to adapt the model prompts to be child-friendly. Striking the right balance between complex AI technology and child-friendly usage was not simple. Particularly, finding an AI-image generation model suitable for kids was difficult. We evaluated models such as DALLE and Stable Diffusio## Inspiration
We built GabbyGarden because we know kids are full of questions and love stories. Sometimes they ask things that even grown-ups don't know. We wanted to make sure they always have someone to talk to, who can answer their questions anytime. So, we made a friendly AI that can chat with them and tell them stories in a fun way. With GabbyGarden, kids can just speak up and listen to stories, making it easy for them to learn and have fun, even if they can't read or write yet. It's like having a smart friend who's always there to explore and learn with them.

## 🎉 Accomplishments that we're proud of
We're immensely proud of creating an interactive and educational platform that captivates children's interests and responds to their curiosity. The development of a multimodal storytelling experience that combines AI-generated audio and visual elements to engage children is a significant accomplishment. We have built a tool that not only entertains but also educates, fostering a love for learning. The seamless integration of advanced AI models to create a responsive and intuitive experience is something that stands out for us.

## 📚 What we learned
Through the development of GabbyGarden, we learned about the importance of user experience, especially when the users are children. We gained insights into how to process and simplify complex AI technology to make it accessible and beneficial for educational purposes. We also learned a lot about prompt engineering and the significance of tailoring interactions to fit the developmental stage of the users. Understanding the ethical considerations and implementing robust privacy measures for children's data was an important part of our learning curve.

## 🌟 What's next for GabbyGarden
Looking ahead, we wish to expand the capabilities of GabbyGarden by adding more educational content and improving the AI's ability to handle a broader range of questions. We are looking to incorporate feedback from real-world users to refine and personalize the learning experience further. Developing additional safety features and parental controls will also be a priority. ## Inspiration


## 🚀 Get Started

To run the app on your own computer:
```
$ source test/bin/activate
$ streamlit run home.py
```