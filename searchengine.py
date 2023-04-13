import os
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring


class SearchEngine:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.schema = Schema(id=ID(stored=True),
                             title=TEXT(stored=True),
                             content=TEXT(stored=True),
                             score=NUMERIC(stored=True))
        self.index = create_in(self.index_dir, self.schema)
        self.searcher = self.index.searcher()
        self.tfidf_scorer = scoring.TF_IDF()

    

    def index_files(self, json_files):
        writer = self.index.writer()
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                #print(str(json_data["title"]))
                writer.add_document(id=str(json_data["paper_id"]),
                                    title=json_data["title"],
                                    content=json_data["abstract"])
        writer.commit()
      

    

    def search(self, query_string):
        parser = QueryParser("title", self.schema)
        query = parser.parse(query_string)
        search_results = self.searcher.search(query)
        #search_results.fragmenter = scoring.Frequency()
        #sorted_results = search_results.top_n(N=len(search_results), reverse=False, key=lambda r: self.tfidf_scoring.score(self.searcher, r, query))

        print(search_results)
       
        return [result["id"] for result in search_results]
    
    #=======Terry==================
    def print_index_contents(self,index):

        with index.searcher() as searcher:
        # Get the document numbers in the index
            docnums = list(searcher.document_numbers())

        # Iterate through the document numbers and print the stored fields
            for docnum in docnums:
                document = searcher.stored_fields(docnum)
                print(document)


if __name__ == "__main__":
    index_dir = "search_index"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    search_engine = SearchEngine(index_dir)
    json_files = ["./parser/formatted_s2orc/JSON_files/file1.json", "./parser/formatted_s2orc/JSON_files/file2.json"]
    search_engine.index_files(json_files)
    search_engine.print_index_contents(search_engine.index)
    print(search_engine.index)
    print(search_engine.search("aerosols"))


# search_engine = SearchEngine(index_dir)

# # search for documents that contain the word "aerosols"
# results = search_engine.search("aerosols")

# # print the document IDs of the matching documents
# print(results)