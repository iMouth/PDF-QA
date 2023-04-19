import os
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh import scoring


class SearchEngine:
    def __init__(self, index_dir):
        self.index_dir = index_dir
        self.schema = Schema(
            id=ID(stored=True), title=TEXT(stored=True), abstract=TEXT(stored=True), score=NUMERIC(stored=True),question=TEXT(stored=True),answer=TEXT(stored=True),section=TEXT(stored=True)
        )
        self.index = create_in(self.index_dir, self.schema)
        self.searcher = self.index.searcher()

    def index_files(self, json_files):
        writer = self.index.writer()
        for file_path in json_files:
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = json.load(f)

                # writer.add_document(id=str(json_data["paper_id"]), title=json_data["title"], abstract=json_data["abstract"],section=json_data["section"])
                # writer.commit()
                
                for i in range(len(json_data["question_answer_pairs"])):
                    writer.add_document(question=json_data["question"][i],answer=json_data["answers"][i])

                
        writer.commit()

    def search(self, query_string):
        parser = QueryParser("answers", self.schema)
        query = parser.parse(query_string)
        tfidf_scoring = scoring.TF_IDF()
        with self.index.searcher() as searcher:
            results = searcher.search(
                query, limit=None, scored=True, terms=True, filter=None, sortedby=["score"], reverse=True
            )
            result_ids = [result["id"] for result in results]
        return result_ids


if __name__ == "__main__":
    index_dir = "search_index"
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    search_engine = SearchEngine(index_dir)
    json_files = [
        "parser/formatted_s2orc/JSON_files/A study of wood burning and traffic aerosols in an Alpine valley using a multi-wavelength Aethalometer.json"
    ]
    search_engine.index_files(json_files)
    
    ids = search_engine.search("What emissions are produced by burning wood?")

    print(ids)
