import json
import os
import sys
import json

PATH = "backend/pdfparser/"


def formatJSON():
    '''
    Formats the JSON file to the format used by the search engine.

    Args:
        None

    Returns:
        None
    '''
    with open(PATH + "pdf-info/" + "file.json", 'r') as f:
        json_data = json.load(f)
        formatted = formatJSON_do(json_data)

    json_files = PATH + "pdf-info/" + "file.json"
    with open(json_files, 'w') as f:
        f.write(formatted)

def formatJSON_do(json_data):
    '''
    Helper function for formatJSON().

    Args:
        json_data (dict): The JSON data to format.

    Returns:
        str: The formatted JSON data.
    '''
    data = {
        "paper_id": json_data['paper_id'],
        "title": json_data['title'],
        "abstract": json_data['abstract'],
        "body_text": []
    }

    add_body_text(json_data, data)

    return json.dumps(data, ensure_ascii=False, indent=4)

def add_body_text(json_data, data):
    '''
    Adds the body text to the JSON data. This includes the section and the text.

    Args:
        json_data (dict): The JSON data to format.
        data (dict): The JSON data to add the body text to.

    Returns:
        None
    '''
    body_text = json_data['pdf_parse']['body_text']
    for body in body_text:
        data['body_text'].append({
            "section": body['section'],
            "text": body['text']
        })


def makePDF(file):
    '''
    Writes the PDF file to the pdf-info directory.

    Args:
        file (File): The PDF file to write.

    Returns:
        None
    '''
    with open (PATH + 'pdf-info/file.pdf', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def parsePDF():
    '''
    Calls the grobid2json script to parse the PDF file. Overwrites the file.json file.

    Args:
        None

    Returns:
        None
    '''
    pdf_dir = PATH + "pdf-info/"
    json_dir = PATH + "pdf-info/"

    l = "python3 " + PATH + "/grobid2json/process_pdf.py -i " 
    r = " -t " + PATH + "temp_dir/ -o " + json_dir

    pdf = "file.pdf"
    pdf = pdf.replace(" ", "\ ").replace("'", "\\'")
    p = l + pdf_dir + pdf + r
    os.system(p)
        
    if os.path.exists(PATH + "temp_dir"): 
        os.system("rm -rf " + PATH + "temp_dir")