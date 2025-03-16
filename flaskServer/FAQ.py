from google import genai
from sentence_transformers import SentenceTransformer
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

FAQ_client = genai.Client(api_key="AIzaSyASczQK9bEiM9zT_gnjU0bRl3qDCH3DfmA")
FAQ_model = 'gemini-2.0-flash'
google_search_tool = Tool(google_search=GoogleSearch())


def FAQ_Agent(query): 
    context = FAQ_client.generate_content(
        model=FAQ_model, 
        contents=query, 
        config=GenerateContentConfig(
            tools=[google_search_tool], 
            response_modalities=['TEXT']
        )
    )
    return context