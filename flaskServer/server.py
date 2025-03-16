from flask import Flask, send_file, request, Response, jsonify
import os
from werkzeug.utils import secure_filename
from Sarvam_api import SarvamAPI
from goog import Gemini
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from store import FaissIndex

app = Flask(__name__)

SA=SarvamAPI()
LLM=Gemini()
#two functions: LLM.send_message(query,img)=>text, LLM.get_chat_history()=>nestedlist

store=FaissIndex()
store.create_index()
global askingQuestion, firstTimeUser, count, msg, intent
firstTimeUser=True
askingQuestion=False
count=0
msg=''
intent=5
questions=["Hey, could you tell me your name?", "Mind sharing how old you are?", "What’s your current salary like? Monthly or yearly, whichever works for you.", "Do you happen to know your credit score, or even just a rough idea of it?", "And how about your work situation? Are you full-time, part-time, self-employed, or something else?"]

#FAQAgentStuff
FAQ_client = genai.Client(api_key="AIzaSyDNBMbKhVjlk62DuUH8BhCsfM_ZVGtABGU")
FAQ_model = 'gemini-2.0-flash'
google_search_tool = Tool(google_search=GoogleSearch())

def FAQ_Agent(query): 
    context = FAQ_client.models.generate_content(
        model=FAQ_model, 
        contents=query, 
        config=GenerateContentConfig(
            tools=[google_search_tool], 
            response_modalities=['TEXT']
        )
    )
    return context

def updated_FAQ(query): 
    text = LLM.send_message(query)

#load the prompt
def check_intent(query):

    def load_prompt(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()

    prompt = load_prompt("prompts/intent.txt").replace("{query}", query)
    
    client = genai.Client(api_key="AIzaSyBc6BbKjBgM6WDnfJ-GKITKAtrUVl4yF6U")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    
    intent = int(response.text)
    return intent

#for members
@app.route("/home/<name>")
def home(name):
    resp={"data":"in home page now", "name":name}
    resp["photo"]=f'/file/{name}'
    return resp

@app.route("/members")
def members():
    return({"data":"this kinda works damn, now i got it from members"})


@app.route("/getfromfiles/<string:filename>")
def getFile(filename):
    filename = secure_filename(filename)
    file_path=os.path.join("./files",filename)
    if os.path.isfile(file_path):
        return send_file(file_path,as_attachment=True)

#uploading files
@app.route("/uploadone", methods=['POST'])
def uploadFile():
    file=request.files['file']
    filename='tempaudio1'+'.'+file.filename.split('.')[-1]
    filename=secure_filename(filename)
    destination="/".join(["./files",filename])
    file.save(destination)
    return {"msg":'done!'}

#recieve message from react
@app.route("/fromuser", methods=['POST'])
def message_from_user():    
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
                output="Thank You For Answering The Questions, You May Ask Me Anything Now."
                askingQuestion=False
                firstTimeUser=False
        else:
            pass

    if intent==3:
        text = store.find_most_relevant_answers(msg)
        if len(text)==0: 
            output=LLM.send_message(f"You are a financial chatbot \nanswer the following question : {msg}\n\n with respect to the given context if any: {text}\n keep it short simple and to the point as its FAQS!")
            store.add_to_index(msg,output)
        else:
            output=text
    if intent==4:
        #miscalleneous
        output=LLM.send_message(msg+"\nYOU ARE A FINANCIAL CHATBOT \n DONT ANSWER QUESTIONS WHICH ARE NOT RELATED TO FINANCE AND LOANS ETC\n say this in a funny way",fpath)
        print(output)
    
    if lang!='en-IN':
        output = SA.translate_text(output,'en-IN',lang)['message']
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