from .pdf_to_json import makePDF, parsePDF, formatJSON
from .search_engine import SearchEngine
import os 
from .api import set_baseurl, ChatCompletion

if os.getenv("FASTCHAT_BASEURL"):
    set_baseurl(os.getenv("FASTCHAT_BASEURL"))
else:
    set_baseurl("http://localhost:8030")

PATH = "backend/pdfparser/"
MAX_HITS = 5
MAX_TOKENS = 500

def build_msg(hits, question):
    '''
    Builds the message to send to the frontend.

    Args:
        hits (list): A list of hits from the search engine.
        question (str): The question to send to the model.

    Returns:
        str: The message to send to the frontend.
    '''
    msg = "You are a chatbot and you are talking to a user.\n\n"
    msg += "The question is: " + question + "\n\n"
    msg += "Use the following as context to answer the question:\n\n"
    msg = msg.split(" ")
    for hit in hits:
        if len(msg) >= MAX_TOKENS:
            break
        msg.extend(hit["text"].split(" "))
        msg.append("\n\n")
    return " ".join(msg[:MAX_TOKENS])

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
        completion = ChatCompletion.create(
            model="vicuna-7b-v1.1",
            messages=[
                {"role": "user", "content": context}
                ]
        )

        return completion.choices[0].message
    except:
        return context

    
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
    