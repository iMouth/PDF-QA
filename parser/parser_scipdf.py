import os
import json
import scipdf
import sys

def pdf_to_json(pdf_path):
    article_dict = scipdf.parse_pdf_to_dict(pdf_path)
    resJson = json.dumps(article_dict, ensure_ascii=False, indent=4)
    return resJson

def parse_pdfs(pdf_dir, json_dir):
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)

    for pdf in os.listdir(pdf_dir):
        if pdf.endswith('.pdf'):
            writeJson = pdf_to_json(pdf_dir + pdf)
            path = json_dir + pdf[:-4] + '.json'
            if os.path.exists(path):
                print('File already exists: ' + path)
                continue
            with open(path, 'w') as f:
                f.write(writeJson)
                

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python3 parser_scipdf.py <pdf_dir> <json_dir>')
        sys.exit(1)

    pdf_dir = sys.argv[1] + '/'
    json_dir = sys.argv[2] + '/'

    if not os.path.exists(pdf_dir):
        print("pdf_dir doesn't exist")
        sys.exit(1)

    parse_pdfs(pdf_dir, json_dir)
