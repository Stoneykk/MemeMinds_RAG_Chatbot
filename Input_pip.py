from transformers import AutoTokenizer, RobertaModel
import torch.nn.functional as F
import openai
import faiss
import numpy as np
from pymongo import MongoClient
from rank_bm25 import BM25Okapi

# Set OpenAI API key
openai.api_key = 'YOUR API KEY HERE'
model = "text-embedding-ada-002"

class Query:

# Embed the input
    def Understand(input_text):

        try:
            response = openai.Embedding.create(
                input=[input_text], 
                model=model
            )

            return np.array(response['data'][0]['embedding'], dtype='float32').reshape(1, -1)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

# Retrive DB by FAISS
    def retrieveFAISS(embedding, k):
        """Retrieve top-k relevant documents from FAISS index and MongoDB."""
        try:
            # Load FAISS index
            index = faiss.read_index("wiki_faiss.index")
            distances, indices = index.search(embedding, k=k)

            # Connect to MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client['RetrivalDB']
            collection = db['wiki_data']

            # Collect matching results
            results = []
            for idx in indices[0]:
                result = collection.find_one({'_id': int(idx)})
                if result:
                    results.append(result)
            
            return results

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []

# Retrive DB by BM25
    def retrieveBM25(options, input_text, n):

        corpus = [option['Summary'] for option in options if 'Summary' in option]

        tokenized_corpus = [doc.split(" ") for doc in corpus]
        bm25 = BM25Okapi(tokenized_corpus)
        
        input_tokens = input_text.split(' ')
        
        top_n_indices = bm25.get_top_n(input_tokens, corpus, n=n)

        # Match the original documents with their indices
        retrieved = [summary for summary in top_n_indices]

        return retrieved

def main():
    input_text = input('Describe your feeling in few sentences:\n')   
    embedding = Query.Understand(input_text)

    if embedding is not None:
        options = Query.retrieveFAISS(embedding, k = 5)
    else:
        print("Failed to generate embedding.")
    
    retrieval = Query.retrieveBM25(options,input_text, n = 1)
    print(retrieval)

if __name__ == "__main__":
    main()