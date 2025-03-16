from google import genai
import PIL.Image
from typing import Optional, Union
from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API = os.getenv("GEMINI_API_KEY")

def load_prompt(path): 
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API)
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
    
    def check_intent(self,query): 
        prompt = (load_prompt("prompts/intent.txt")).replace("{query}", query)
        response = self.chat.send_message(prompt)
        temp = int(response.text)
        return temp
    
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

        #x = self.check_intent(message)

        return response.text
 
    
    def get_chat_history(self) -> list:
        history = []
        for message in self.chat._curated_history:
            history.append(f'role - {message.role}: {message.parts[0].text}')
        return history

"""
How To Use? 
#Variables : query, image_path, chat_history

LLM = Gemini(api)

response_for_text = LLM.send_text_message(query) -> str
response_for_image = LLM.send_text_with_image(query, image_path) -> str
chat_history = LLM.get_chat_history()   -> list
"""

if __name__=="__main__":
    LLM=Gemini()
    query="hello, how are you"
    response=LLM.send_message(query)
    print(response)