import os 
import PIL.Image

from google import genai
from dotenv import load_dotenv
load_dotenv()
from typing import Optional, Union

GEMINI_API_1 = os.getenv("GEMINI_API_1") #Main Gemini_API
GEMINI_API_2 = os.getenv("GEMINI_API_2") #Intent Checking_API

def load_prompt(path): 
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_1)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")

    def send_message(self, message: str, image_path: Optional[str] = None) -> str:
        if image_path:
            try:
                image = PIL.Image.open(image_path)
                response = self.chat.send_message([message, image])

            except FileNotFoundError:
                return "Error: Image file not found."
            except Exception as e:
                return f"Error opening image: {e}"
            
        else:
            response = self.chat.send_message(message)

        return response.text
    
    def get_chat_history(self) -> list:
        history = []
        for message in self.chat._curated_history:
            history.append(f'{message.role}: {message.parts[0].text}')
        return history

llm = Gemini()
