import json
import os
import sys

def add_body_text(json_data, data):
    body_text = json_data['pdf_parse']['body_text']
    for body in body_text:
        data['body_text'].append({
            "section": body['section'],
            "text": body['text']
        })


def add_qa_files(qa_files, data):
    with open(qa_files, 'r') as f:
        f = f.readlines() + ['\n']
        qa = {}
        for line in f:
            if line == "\n": 
                for q in qa:
                    data['question_answer_pairs'].append({
                        "question": q,
                        "answers": qa[q]
                    })
                qa = {}
            elif line.startswith("Q:"):
                q = line[2:].strip()
                qa[q] = []
            elif line.startswith("A:"):
                a = line[2:].strip()
                qa[q].append(a)

def formatter(json_data, qa_files = None):
    data = {
        "paper_id": json_data['paper_id'],
        "title": json_data['title'],
        "abstract": json_data['abstract'],
        "question_answer_pairs": [],
        "body_text": []
    }

    add_body_text(json_data, data)

    if qa_files:
        add_qa_files(qa_files, data)
                
    return json.dumps(data, ensure_ascii=False, indent=4)

def format_json(json_dir, target_dir):
    for json_file in os.listdir(json_dir):
        if json_file.endswith('.json'):
            qa_files = target_dir + "QA_files/" + json_file[:-5] + ".txt"
            if not os.path.exists(qa_files):
                with open(qa_files, 'a') as f: pass
            
            with open(json_dir + json_file, 'r') as f:
                json_data = json.load(f)
                formatted = formatter(json_data, qa_files)
               
            json_files = target_dir + "JSON_files/" + json_file
            with open(json_files, 'w') as f:
                f.write(formatted)
               

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 format.py <json_dir> <target_dir>")
        sys.exit(1)

    json_dir = sys.argv[1] + '/'
    if not os.path.exists(json_dir):
        print("json_dir doesn't exist")
        sys.exit(1)

    target_dir = sys.argv[2] + '/'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        os.makedirs(target_dir + "JSON_files/")
        os.makedirs(target_dir + "JSON_files/")
    else:
        if not os.path.exists(target_dir + "JSON_files/"):
            os.makedirs(target_dir + "JSON_files/")
        if not os.path.exists(target_dir + "QA_files/"):
            os.makedirs(target_dir + "QA_files/")

    format_json(json_dir, target_dir)

if __name__ == '__main__':
    main()
