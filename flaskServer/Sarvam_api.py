#importing the required libraries
import requests
import json
from dotenv import load_dotenv
import os
import base64
import wave

#loading the environment variables
load_dotenv()


class SarvamAPI:

    def __init__(self):
        self.api_key = os.getenv("SARVAM_API_KEY") #getting the api key from the environment variables
        self.base_url ="https://api.sarvam.ai/" #base url of the api

#function to translate the text
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
            response = requests.request("POST", url, json=payload, headers=headers) #sending the post request to sarvam api
            data=response.json()

            if "error" in data:
                return {"status":"error", "message":data["error"]["code"]}
            else:
                return {"status":"success", "message":data["translated_text"]}

        except requests.exceptions.RequestException as e:
            return{"status":"error", "message":{str(e)}}
        



        # print(response.json().get("translated_text", "")) #testing
        # print(response.status_code) #testing
        



#function to convert speech to text and translate it        
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





#fucntion to convert text to speech
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
            #parse audio wav file
            if response.status_code !=200:
                return {"status":"error", "message":response.json()["error"]["code"]}
            else:
                return {"status":"success", "message":response.json()["audios"][0]}
            
            # audio = response.json()["audios"][0]
            # audio = base64.b64decode(audio)

            # #creating file
            # with wave.open(f"output.wav", "wb") as wav_file:
            #     # Set the parameters for the .wav file
            #     wav_file.setnchannels(1)  # Mono audio
            #     wav_file.setsampwidth(2)  # 2 bytes per sample
            #     wav_file.setframerate(22050)  # Sample rate of 22050 Hz

            #     # Write the audio data to the file
            #     wav_file.writeframes(audio)
        
        except requests.exceptions.RequestException as e:
            return {"status":"error", "message":str(e)}


if __name__=='__main__':
    #TESTING
    sarvam=SarvamAPI()
    print(sarvam.translate_text("हे, क्या चल रहा है","hi-IN", "en-IN"))
    # sarvam.speech_to_text_translate("../10087.mp3")

    # text="ಹಾಯ್ ನಾನು ಕುಶಾಲ್, ಹೇಗಿದ್ದೀಯಾ?"
    # sarvam.text_to_speech(text, "kn-IN")

    #TO DO
    #1.NEED to add error handling yet to be done

    
