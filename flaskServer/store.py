import os
import faiss 
import pickle 
import numpy as np 

from google import genai
from sentence_transformers import SentenceTransformer
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

class FaissIndex:
    def __init__(self, index_path="Session/FAQ/faiss_index.bin", data_path="Session/FAQ/data.pkl"):
        self.index_path = index_path
        self.data_path = data_path
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384 
        self.index = faiss.IndexFlatL2(self.dimension)
        self.data = []
    
    def create_index(self):
        question, answer = "",""
        self.add_to_index(question, answer)
    
    def add_to_index(self, question, answer):
        embedding = self.model.encode([question]).astype(np.float32)
        self.index.add(embedding)
        self.data.append((question, answer))
        self.save_index()
    
    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.data_path, "wb") as f:
            pickle.dump(self.data, f)
    
    def load_index(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.data_path, "rb") as f:
            self.data = pickle.load(f)
    
    def find_most_relevant_answers(self, query, k=1):
        query_embedding = self.model.encode([query]).astype(np.float32)
        distances, indices = self.index.search(query_embedding, k)
        results = [(self.data[i][0], self.data[i][1]) for i in indices[0] if i < len(self.data)]
        return results
        
if __name__=='__main__':
    store=FaissIndex()
    store.create_index()