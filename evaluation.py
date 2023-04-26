import whoosh.index as index
from whoosh.qparser import QueryParser
import json
import nltk.translate.bleu_score as bleu

# Load the Whoosh index
ix = index.open_dir("path/to/index")

# Load the questions and answers from the JSON file
with open("path/to/json_file.json") as f:
    data = json.load(f)

# Define the number of answers to retrieve
k = 5

for q_a_pair in data:
    # Get the question and actual answer from the JSON file
    question = q_a_pair['question']
    actual_answer = q_a_pair['answer']
    
    # Define the search query
    query = QueryParser("content", ix.schema).parse(question)
    
    # Perform the search and retrieve the top k answers
    with ix.searcher() as searcher:
        results = searcher.search(query, limit=k)
        candidate_answers = [hit['content'] for hit in results]
    
    # Tokenize and preprocess the reference answer
    reference_tokens = nltk.word_tokenize(actual_answer.lower())
    
    # Calculate the BLEU score for each candidate answer
    bleu_scores = []
    for candidate_answer in candidate_answers:
        # Tokenize and preprocess the candidate answer
        candidate_tokens = nltk.word_tokenize(candidate_answer.lower())
        
        # Calculate the BLEU score
        bleu_score = bleu.sentence_bleu([reference_tokens], candidate_tokens)
        bleu_scores.append(bleu_score)
    
    # Get the index of the candidate answer with the highest BLEU score
    max_bleu_index = bleu_scores.index(max(bleu_scores))
    
    # Print the question, actual answer, and best candidate answer
    print("Question:", question)
    print("Actual answer:", actual_answer)
    print("Best candidate answer:", candidate_answers[max_bleu_index])
    print("BLEU score:", max(bleu_scores))
    print("-------------------------------")
