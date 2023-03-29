import os

if __name__ == "__main__":
    l = "python3 s2orc-doc2json/doc2json/grobid2json/process_pdf.py -i " 
    r = " -t temp_dir/ -o test_s2orc-doc2json/"
    pdf_dir = "test_pdfs/"


    for pdf in os.listdir(pdf_dir):
        pdf = pdf.replace(" ", "\ ")
        p = l + pdf_dir + pdf + r
        os.system(p)

    if os.path.exists("temp_dir"): 
        os.system("rm -rf temp_dir")