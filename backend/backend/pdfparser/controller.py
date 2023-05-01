from .pdf_to_json import makePDF, parsePDF, formatJSON
from .search_engine import SearchEngine
import os 
# from .api import set_baseurl, ChatCompletion
import sys

sys.path.append("..")
sys.path.append("../FastChat/")
sys.path.append("../FastChat/fastchat/")
sys.path.append("../FastChat/fastchat/client/")

from FastChat.fastchat import client
import requests

## get CHAT_GPT_KEY from .env

from dotenv import load_dotenv
load_dotenv()

CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")

if os.getenv("FASTCHAT_BASEURL"):
    client.set_baseurl(os.getenv("FASTCHAT_BASEURL"))
else:
    client.set_baseurl("http://localhost:8030")

PATH = "backend/pdfparser/"
MAX_HITS = 3
MAX_TOKENS = 350

def build_msg(hits, question):
    '''
    Builds the message to send to the frontend.

    Args:
        hits (list): A list of hits from the search engine.
        question (str): The question to send to the model.

    Returns:
        str: The message to send to the frontend.
    '''
    msg = "You are ChatGPT, a large language model trained by OpenAI. Your task is to answer questions based on the given context. Please answer the following question based on the context provided.\n\n"
    msg += "Use the following as context to answer the question:\n\n"
    msg += "Example: \n\n"
    msg += "Context: \n\n"
    msg += "On a sunny day, a group of friends decided to have a picnic by the lake. They brought sandwiches, salads, and a variety of fruits to share. They spent the afternoon playing frisbee, swimming, and sunbathing. \n\n"
    msg += "Question: \n\n"
    msg += "What did the group of friends bring to the picnic? \n\n"
    msg += "Answer: \n\n"
    msg += "According to the provided context, the group of friends prepared an assortment of delicious items for their picnic by the lake. They packed a selection of sandwiches, an array of salads, and a diverse range of fruits to share among themselves, ensuring that everyone could enjoy the pleasant outdoor dining experience. \n\n"
    msg += "Context: \n\n"
    msg = msg.split(" ")
    for hit in hits:
        if len(msg) >= MAX_TOKENS:
            break
        msg.extend(hit["text"].split(" "))
        msg.append("\n\n")
    
    msg = " ".join(msg[:MAX_TOKENS])
    msg += "\n\n"

    msg += "Question: \n\n"
    msg += question + "\n\n"
    msg += "Answer: \n\n"
    return msg

def get_message(question):
    '''
    Gets the message to send to the model.

    Args:
        question (str): The question to send to the model.

    Returns:
        str: The message to send to the model.
    '''
    index_dir = PATH + "search_index"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
   
    search_engine = SearchEngine(index_dir)
    json_file = PATH + "pdf-info/file.json"
    search_engine.index_files(json_file)

    hits = search_engine.search(question, limit=None, top_n=MAX_HITS)

    if os.path.exists(PATH + "search_index"): 
        os.system("rm -rf " + PATH + "search_index")

    return build_msg(hits, question)
    
def get_anwser(context):
    '''
    Gets the answer to the question.

    Args:
        context (str): The context to send to the model.

    Returns:
        str: The answer to the question.
    '''

    try:
        completion = client.ChatCompletion.create(
            model="vicuna-13b-v1.1",
            messages=[
                {"role": "user", "content": context}
                ],
            stream=True
            
        )
        return completion
    
    except:
        if not CHATGPT_API_KEY:
            return "FastChat model is not working please add a CHAT_GPT key to enviroment variables to use Chat GPT. Context to be sent below.\n\n" + context
        try: 
            url = 'https://api.openai.com/v1/completions'

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {CHATGPT_API_KEY}',
            }

            data = {
                "model": "gpt-3.5-turbo",
                "prompt": context,
                "max_tokens": 200,
                "temperature": 0.5,
            }

            response = requests.post(url, headers=headers, json=data)
            return response.json()["choices"][0]["text"]
        except:
            return "CHAT GPT and FastChat model is not working. Context to be sent below.\n\n" + context


    
def main(file_pdf):
    '''
    Main function for the PDF parser. This function calls the functions to make the PDF, parse the PDF, and format the JSON.

    Args:
        file_pdf (str): The path to the PDF file to parse.

    Returns:
        None
    '''
    makePDF(file_pdf)
    parsePDF()
    formatJSON()
    