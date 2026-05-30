import pandas as pd
import chromadb as ch
import uuid
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
class Portfolio:
    def __init__(self, file_path = "app/resources/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = ch.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name = 'portfolio', embedding_function=ef)
    
    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents = [row['Techstack']],
                            metadatas=[{'Links' : row['Links']}],
                            ids = [str(uuid.uuid4())])
    
    def query_links(self, skills):
        return self.collection.query(query_texts = skills, n_results = 2).get('metadatas', [])
    
    