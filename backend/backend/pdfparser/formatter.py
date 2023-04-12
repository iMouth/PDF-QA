import json
import os
import sys
import json

PATH = "backend/pdfparser/"

def add_body_text(json_data, data):
    body_text = json_data['pdf_parse']['body_text']
    for body in body_text:
        data['body_text'].append({
            "section": body['section'],
            "text": body['text']
        })

def formatter(json_data):
    data = {
        "paper_id": json_data['paper_id'],
        "title": json_data['title'],
        "abstract": json_data['abstract'],
        "body_text": []
    }

    add_body_text(json_data, data)

    return json.dumps(data, ensure_ascii=False, indent=4)

def makePDF(file):
    with open (PATH + 'pdf-info/file.pdf', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def parsePDF():
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

def formatJSON():
    with open(PATH + "pdf-info/" + "file.json", 'r') as f:
        json_data = json.load(f)
        formatted = formatter(json_data)

    json_files = PATH + "pdf-info/" + "file.json"
    with open(json_files, 'w') as f:
        f.write(formatted)

def main(file):
    makePDF(file)
    parsePDF()
    formatJSON()
