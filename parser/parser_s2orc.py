import sys
import os


def main():
    if len(sys.argv) < 3:
        print("Usage python3 parser-s2orc.py <pdf_dir> <json_dir>")
        sys.exit(1)

    pdf_dir = sys.argv[1] + "/"
    json_dir = sys.argv[2] + "/"

    l = "python3 s2orc-doc2json/doc2json/grobid2json/process_pdf.py -i " 
    r = " -t temp_dir/ -o " + json_dir

    for pdf in os.listdir(pdf_dir):
        if os.path.exists("test_s2orc/" + pdf[:-4] + ".json"):
            continue
        pdf = pdf.replace(" ", "\ ").replace("'", "\\'")
        p = l + pdf_dir + pdf + r
        os.system(p)

    if os.path.exists("temp_dir"): 
        os.system("rm -rf temp_dir")

if __name__ == "__main__":
    main()