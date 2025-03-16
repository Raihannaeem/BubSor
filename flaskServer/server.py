import os
import sys
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_2 = os.getenv("GEMINI_API_2") #INTENT_CHECK
GEMINI_API_3 = os.getenv("GEMINI_API_3") #SCRAPPER_1
GEMINI_API_4 = os.getenv("GEMINI_API_4") #SCRAPPER_1

from SARVAM import SarvamAPI

from LLM import Gemini
from google import genai
from google.genai import types
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

from werkzeug.utils import secure_filename
from flask import Flask, send_file, request, Response, jsonify


def scrapper(query):
    try:
        scraper_client = genai.Client(api_key=GEMINI_API_3)
        response = scraper_client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Scrape all the related information about the query!\nquery:{query}",
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                google_search=types.GoogleSearchRetrieval
                )]
            )
        )
    except: 
        scraper_client = genai.Client(api_key=GEMINI_API_4)
        response = scraper_client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f"Scrape all the related information about the query!\nquery:{query}",
        config=types.GenerateContentConfig(
            tools=[types.Tool(
                google_search=types.GoogleSearchRetrieval
                )]
            )
        )

    return response.text

app = Flask(__name__)
SA = SarvamAPI()
LLM = Gemini()

global askingQuestion, firstTimeUser, count, msg, intent

firstTimeUser=True
askingQuestion=False
count=0

msg=''
intent=5
questions=["Yeah Sure, could you tell me your name to start of with?", "Mind sharing how old you are?", "What’s your current salary like? Monthly or yearly, whichever works for you.", "Do you happen to know your credit score, or even just a rough idea of it?", "And how about your work situation? Are you full-time, part-time, self-employed, or something else?"]

def check_intent(query):

    def load_prompt(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    prompt = load_prompt("prompts/intent.txt").replace("{query}", query)
    
    client = genai.Client(api_key=GEMINI_API_2)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    intent = int(response.text)
    return intent

@app.route("/reset")
def reset():
    os.execv(sys.executable, ['python'] + sys.argv)

@app.route("/test")
def members():
    return({"data":"this kinda works damn, testing testing"})

@app.route("/fromuser", methods=['POST'])
def message_from_user():    
    audio_output=''
    global askingQuestion, firstTimeUser, count, intent, msg
    lang=request.form.get('language')
    msg=request.form.get('text')
    files = request.files.getlist("file")
    fpath=None
    print(request.form)
    if request.form.get('type')=='text' and msg!='':
        if lang!='en-IN':
            #output+=' translated'
            #msg="translated text"
            msg=SA.translate_text(msg,lang,'en-IN')['message']
    elif request.form.get('type')=='audio':
        for file in files:
            if file.filename.split('.')[-1]=='wav':
                saobj=SA.speech_to_text_translate(file)
                msg=saobj['message']
                lang=saobj['language']
                #print(msg)
                #print(lang)
        #output+=' audio'
        #audio_file=request.files['file']
        #msg="audiototext"
    if request.form.get('isFile')=='y':
        #output+=' file'
        for file in files:
            if file.filename.split('.')[-1]!='wav':
                filename='temp.'+file.filename.split('.')[-1]
                filename=secure_filename(filename)
                destination="/".join(["./session",filename])
                file.save(destination)
        fpath=f'./session/{filename}'


    if askingQuestion==False:
        intent=check_intent(msg)

    if intent==1 or intent==2:

        if firstTimeUser:
            if count<=4:
                output=questions[count]
                if count!=0:
                    temp=LLM.send_message(questions[count-1]+":"+msg,None)
                
                count+=1
                askingQuestion=True
    
            else:
                temp=LLM.send_message(questions[count-1]+":"+msg,None)
                output="Thank You For Answering The Questions, You May Ask Me Anything Now!"
                askingQuestion=False
                firstTimeUser=False
            
        else:
            scrapped = scrapper(msg) 
            cleaned = LLM.send_message(f"You are a FINANCIAL DATA Cleaning Agent \nClean the following data to make it visually appealing \ndata : {scrapped}")
            summary = LLM.send_message(f"You are a FINANCIAL SUMMARIZING Agent \nSummarize the following data and make sure to keep it within 500 CHARACTERS \ndata : {cleaned}")

            output = cleaned 
            audio_output = summary

    if intent==3:
        #RAG
        """
        if: 
        else: 
        """
        prompt = f"You are a FINANCIAL CHATBOT, answer the following question in a short and summarized manner with respect to FINANCE ONLY\nquery:{msg}\nKeep it short and simple to the point as it is in FAQs!" 
        output = LLM.send_message(prompt,fpath)
        
        #print(output)
    
    if intent==4: #MISC
        prompt = f"You are a FINANCIAL CHATBOT, answer the following question in a short and summarized manner with respect to FINANCE ONLY\nquery:{msg}\nDONT answer questions which are NOT related to finance/banks/loans, tell a simple JOKE instead." 
        output = LLM.send_message(prompt,fpath)
        
        #print(output)
    
    if lang!='en-IN':
        output = SA.translate_text(output,'en-IN',lang)['message']
    if audio_output:
        if lang!='en-IN':
            output = SA.translate_text(audio_output,'en-IN',lang)['message']
        audio = "SA.text_to_speech(audio_output,lang)['message']"
    else:
        audio = "SA.text_to_speech(output,lang)['message']"


    print(msg)
    print(output)

    response_json={
        "data":output,
        "audio_base64":audio
    }

    return jsonify(response_json)

if __name__=='__main__':
    app.run(debug=True)