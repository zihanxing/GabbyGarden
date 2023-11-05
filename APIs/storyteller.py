import openai
import os
import json
import random

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.getenv('OPENAI_API_KEY')


def ask_openai(messages, temperature=0.5):
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-4",
            messages=messages,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        return "I'm sorry, but I can't answer that question."


def storyteller():
    json_file = open("storyQ.json", "r")
    pre_questions = json.load(json_file)
    q_list = pre_questions['questions']
    json_file.close()

    

    print("Hello! Welcome to GabbyGarden! I am Gab. To listen to a story, please answer me the question.")

    conversation_log = [] # to maintain the conversation context
    
    context = "You are a chatbot telling stories to young kids.\n\
        I will provide you a question and answer from the kid. \
        Based on the answer, you will tell a funny story to the kid. \n\
        As I am going to split the story into 3 parts, please provide a very short story with 3 short paragraphs respectively."

    conversation_log.append({"role": "system", "content": context})


    count = 0
    while True:
        if count == 0:
            q = random.choice(q_list)
            conversation_log.append({"role": "assistant", "content": q})
            answer = input(q)
        else:
            answer = input('Please respond (or enter "end" to stop)')

        if answer.lower() == 'end':
            break

    
        conversation_log.append({"role": "user", "content": answer})

        # Get the chatbot's response and print it
        bot_response = ask_openai(conversation_log)


        print("Answer:", bot_response)

        # Add the chatbot's response to the conversation log
        conversation_log.append({"role": "assistant", "content": bot_response})

        count += 1

def main():
    storyteller()

if __name__ == '__main__':
    main()




