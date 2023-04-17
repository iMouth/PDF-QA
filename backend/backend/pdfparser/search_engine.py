from whoosh.index import create_in, open_dir
from whoosh.fields import TEXT, ID, Schema
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from whoosh import scoring
from whoosh.analysis import StemmingAnalyzer, StandardAnalyzer, NgramAnalyzer, LowercaseFilter, StopFilter
import json

class SearchEngine:
    def __init__(self, index_dir):
        '''
        Initializes the search engine.
        '''
        self.schema = Schema(
                        paper_id=ID(stored=True),
                        title=TEXT(stored=True),
                        abstract=TEXT(stored=True),
                        section=TEXT(stored=True),
                        text=TEXT(
                            analyzer=NgramAnalyzer(4) | LowercaseFilter() | StopFilter(), 
                            stored=True
                            )
                        )
        
        self.index_dir = index_dir
        try:
            self.index = open_dir(index_dir)
        except:
            self.index = create_in(index_dir, self.schema)
        
        self.searcher = self.index.searcher(weighting=scoring.BM25F)
    
    def index_files(self, json_file):
        '''
        Indexes the JSON files in the index directory.

        Args:
            json_files (list): A list of JSON files to index.

        Returns:
            None
        '''
        writer = self.index.writer()
        with open(json_file, 'r', encoding="utf-8") as f:
            data = json.load(f)
            for paragraph in data["body_text"]:
                writer.add_document(
                    paper_id=data["paper_id"], 
                    title=data["title"], 
                    abstract=data["abstract"], 
                    section=paragraph["section"], 
                    text=paragraph["text"],
                        )
        writer.commit()
    
    def search(self, query_string, limit=None, top_n=1):
        '''
        Searches the index for the query string and returns the top N results.

        Args:
            query_string (str): The query string to search the index with.
            limit (int, optional): the maximum number of documents to score.
            top_n (int, optional): The number of top results to return. Defaults to 1.

        Returns:
            list: A list of dictionaries containing the results. Each dictionary contains the paper_id, title, abstract, section, and text.
        '''
        parser = QueryParser("text", schema=self.schema, group=OrGroup)
        query = parser.parse(query_string)
        
        with self.index.searcher() as searcher:
            results = searcher.search(
                        query, 
                        limit=limit,
                        scored=True, 
                        terms=True, 
                        filter=None, 
                        sortedby=["text"], 
                        reverse=True
                        )
            results = list(results)
            results.sort(key=lambda hit: 
                        (len(hit.matched_terms()), 
                        hit.score), 
                        reverse=True)
            results = results[0:top_n]
            results = [dict(result) for result in results]

        return results
        
    def print_index(self, query_string=None, limit=None):
        '''
        Prints the index to the console if no query string is provided.
        If a query string is provided, prints the results of the query. Including the section, text, and score.

        Args:
            query_string (str, optional): The query string to search the index with. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to None.

        Returns:
            None
        '''
        if query_string is not None:
            parser = QueryParser("text", schema=self.schema, group=OrGroup)
            query = parser.parse(query_string)
            with self.index.searcher() as searcher:
                results = searcher.search(
                            query, 
                            limit=limit,
                            scored=True, 
                            terms=True, 
                            filter=None, 
                            sortedby=["text"], 
                            reverse=True
                            )
                results = list(results)
                results.sort(key=lambda hit: 
                            (len(hit.matched_terms()), 
                            hit.score), 
                            reverse=True)
                for hit in results:
                    print("SECTION:", hit["section"])
                    print("TEXT:", hit["text"][0:100], "...")
                    print("HITS:", hit.matched_terms())
                    print("SCORE:", hit.score)
                    print()
        else:
            with self.index.searcher() as searcher:
                for fields in searcher.all_stored_fields():
                    print(fields)