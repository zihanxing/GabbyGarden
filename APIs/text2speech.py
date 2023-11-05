import requests
import urllib.request

# text = "Hi there, welcome to Genny. The Simple mode is perfect for creating single speaker short voiceovers. Simply pick your preferred speaker, type or copy and paste your script. Then, click the 'Generate' button to generate your voiceover in seconds. You will see the voiceover output on the right for you to freely share or download. For more advanced capabilities, video editing, or longer multi-speaker voiceover production, please checkout the Advanced mode instead. "

        
def get_speech_from_text(text):
    # settings
    speaker = "63b407a8241a82001d51b977"
    speed = 0.85
    API_key= "60cd1344-2f53-47c7-a205-5bb8e3e03822"
    
    url = "https://api.genny.lovo.ai/api/v1/tts/sync"
    payload = {  
        "speed": speed,
        "text": text,    
        "speaker": speaker, 
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": API_key
    }

    TTS_response = requests.post(url, json=payload, headers=headers)

    # retrive_url =  urllib.parse.urljoin("https://api.genny.lovo.ai/api/v1/tts/", TTS_response.json()["id"])
  
    retrive_url =  urllib.parse.urljoin("https://api.genny.lovo.ai/api/v1/tts/sync", TTS_response.json()["id"])

    headers = {
        "x-api-key":API_key,
        "accept": "application/json"
    }
  
    retrive_response = requests.get(retrive_url, headers=headers)
  
    speech_url = retrive_response.json()["data"][0]["urls"][0]
    urllib.request.urlretrieve(speech_url, "/Users/macbookp/Desktop/Duke/Semester2023fall/AI_Hackathon/Hack/assets/speech.mp3")