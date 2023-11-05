import requests
import urllib.request
from underthesea import sent_tokenize
import os
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from pathlib import Path


def concatenate_strings(input_strings):
    result = []
    current_concatenation = input_strings[0]
    
    for string in input_strings[1:]:
        if len(current_concatenation + string) <= 500:
            current_concatenation += string
        else:
            result.append(current_concatenation)
            current_concatenation = string
    
    result.append(current_concatenation)
    return result

def concatenate_wav_files(input_files, output_file):
    # Read the first WAV file to get the sample rate and audio data type
    sample_rate, audio_data = wavfile.read(input_files[0])
    audio_dtype = audio_data.dtype

    # Initialize an empty array to store concatenated audio data
    concatenated_audio = audio_data

    # Iterate through the remaining input files and concatenate audio data
    for input_file in input_files[1:]:
        _, audio_data = wavfile.read(input_file)

        # # Ensure the sample rates and data types match before concatenating
        # if audio_data.dtype != audio_dtype or audio_data.shape[1] != concatenated_audio.shape[1]:
        #     raise ValueError("Incompatible audio formats. Sample rates and data types must match.")

        concatenated_audio = np.concatenate((concatenated_audio, audio_data))

    # Write the concatenated audio data to the output file
    wavfile.write(output_file, sample_rate, concatenated_audio)
        
def get_speech_from_text(text, filename=None):
  
    speaker = "63b407a8241a82001d51b977"
    speed = 1.1
    API_key= "a6221301-a711-45c9-b533-cf0596fc3318"
  
    cur_path = Path(os.getcwd())
    sent_list = sent_tokenize(text)
    sent_concatenated = concatenate_strings(sent_list)
    
    mp3_files = []

    for i, sent in enumerate(sent_concatenated):
        url = "https://api.genny.lovo.ai/api/v1/tts/sync"
        payload = {  
        "speed": speed,
        "text": sent,    
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
        urllib.request.urlretrieve(speech_url,   cur_path / Path(f"assets/speech_{i}" + ".wav"))
        mp3_files.append(cur_path / Path(f"assets/speech_{i}" + ".wav"))
    print(mp3_files)
    input_files = mp3_files
    if filename:
        output_files = cur_path / Path(f"assets/{filename}.mp3")
    else:
        output_files = cur_path / Path(f"assets/speech.mp3")
    concatenate_wav_files(input_files, output_files)
        
        
    