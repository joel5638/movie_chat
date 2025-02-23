import chromadb
from chromadb.utils import embedding_functions
import pandas as pd

class MovieVectorStore:
    def __init__(self, api_key: str):
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="movies",
            embedding_function=self.embedding_fn
        )
        self.df = None

    def add_movies(self, df: pd.DataFrame) -> None:
        self.df = df.copy()
        
        if self.collection.count() == 0:
            documents = []
            metadatas = []
            ids = []
            
            for idx, movie in df.iterrows():
                doc = f"""
                Title: {movie['Series_Title']}
                Year: {movie['Released_Year']}
                Director: {movie['Director']}
                Genre: {movie['Genre']}
                Rating: IMDB {movie['IMDB_Rating']}, Meta {movie['Meta_score']}
                Cast: {movie['Star1']}, {movie['Star2']}, {movie['Star3']}, {movie['Star4']}
                Overview: {movie['Overview']}
                """
                
                meta = {
                    "title": str(movie['Series_Title']),
                    "director": str(movie['Director']),
                    "year": str(movie['Released_Year']),
                    "genre": str(movie['Genre']),
                    "rating": str(movie['IMDB_Rating'])
                }
                
                documents.append(doc)
                metadatas.append(meta)
                ids.append(f"movie_{idx}")
            
            batch_size = 50
            for i in range(0, len(documents), batch_size):
                end = min(i + batch_size, len(documents))
                self.collection.add(
                    documents=documents[i:end],
                    metadatas=metadatas[i:end],
                    ids=ids[i:end]
                )

    def search(self, query: str, n_results: int = 5) -> dict:
        try:
            if "director" in query.lower():
                director_name = query.lower().split("director")[-1].strip()
                results = self.collection.query(
                    query_texts=[query],
                    where={"director": director_name},
                    n_results=10
                )
            else:
                results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results
                )
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return {
                'documents': [["No results found. Please try again."]],
                'metadatas': [[]]
            }