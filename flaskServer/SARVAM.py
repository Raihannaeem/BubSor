import os 
import json 
import wave
import base64
import requests 

from dotenv import load_dotenv
load_dotenv()

class SarvamAPI:
    def __init__(self):
        self.api_key = os.getenv("SARVAM_API")
        self.base_url ="https://api.sarvam.ai/" 

    def translate_text(self, input:str, source_language_code:str, target_language_code:str): 
        endpoint = "translate"
        url = self.base_url + endpoint

        payload = {
                "input": input,
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
                "speaker_gender": "Male",
                "mode": "code-mixed",
                "model": "mayura:v1",
                "enable_preprocessing": False,
                "output_script": "fully-native"
                }   
        
        headers = {
                "Content-Type": "application/json",
                "api-subscription-key": self.api_key
                }
        try:
            response = requests.request("POST", url, json=payload, headers=headers)
            data=response.json()

            if "error" in data:
                return {"status":"error", "message":data["error"]["code"]}
            else:
                return {"status":"success", "message":data["translated_text"]}
        except requests.exceptions.RequestException as e:
            return{"status":"error", "message":{str(e)}}
        
    def speech_to_text_translate(self, file):
        endpoint = "speech-to-text-translate"
        url = self.base_url + endpoint

        data = {
            "model":"saaras:v1"
        }

        headers = {
            "api-subscription-key": self.api_key
        }
        files = {"file": ("audio.mp3", file, "audio/mpeg")}

        try:
            response = requests.post(url, headers=headers, data=data, files=files) #sending the post request to sarvam api
            data=response.json()

            if "error" in data:
                return {"status":"error", "message":data["error"]["code"]}
            else:
                return {"status":"success", "message":data["transcript"], "language":data["language_code"]}
        except requests.exceptions.RequestException as e:
            return{"status":"error", "message":{str(e)}}

    def text_to_speech(self, inputs:str, target_language_code:str):
        endpoint = "text-to-speech"
        url = self.base_url + endpoint

        payload = {
            "inputs": [inputs,],  # Text to convert to speech
            "target_language_code": target_language_code,  # Target language code
            "speaker": "meera",  # Speaker voice
            "model": "bulbul:v1",  # Model to use
            "pitch": 0,  # Pitch adjustment
            "pace": 1.0,  # Speed of speech
            "loudness": 1.0,  # Volume adjustment
            "enable_preprocessing": True,  # Enable text preprocessing
        }

        headers = {
            "Content-Type": "application/json",
            "api-subscription-key": self.api_key
        }
        try:
            response= requests.post(url, json=payload, headers=headers)

            if response.status_code !=200:
                return {"status":"error", "message":response.json()["error"]["code"]}
            else:
                return {"status":"success", "message":response.json()["audios"][0]}
        except requests.exceptions.RequestException as e:
            return {"status":"error", "message":str(e)}