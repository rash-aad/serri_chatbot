# src/knowledge_base/vector_store.py

import chromadb
from sentence_transformers import SentenceTransformer

class VectorStoreManager:
    def __init__(self, collection_name="serri_docs"):
        """
        Initializes the VectorStoreManager.

        Args:
            collection_name (str): The name of the collection to use in ChromaDB.
        """
        print("Initializing VectorStoreManager...")
        # Initialize the embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Embedding model loaded.")
        
        # Initialize the ChromaDB client. We'll use a persistent client that saves to disk.
        self.client = chromadb.PersistentClient(path="./chroma_db")
        print(f"ChromaDB client initialized. Data will be stored in './chroma_db'.")
        
        # Get or create the collection
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print(f"Collection '{collection_name}' loaded/created.")

    def populate_collection(self, document_chunks: list[dict]):
        """
        Generates embeddings for document chunks and stores them in the collection.
        This will clear any existing data in the collection before adding new data.

        Args:
            document_chunks (list[dict]): A list of document chunks from the loader.
        """
        # First, let's check if the collection already has documents.
        # If we are re-populating, it's good practice to clear it first.
        if self.collection.count() > 0:
            print(f"Collection already contains {self.collection.count()} documents. Clearing...")
            # This is a workaround as ChromaDB's delete can be complex.
            # We will delete the collection and recreate it.
            self.client.delete_collection(name=self.collection.name)
            self.collection = self.client.create_collection(name=self.collection.name)
            print("Collection cleared.")

        print(f"Processing {len(document_chunks)} chunks to populate the collection...")
        
        # Prepare the data for ChromaDB
        ids = [str(i) for i in range(len(document_chunks))]
        texts = [chunk['text'] for chunk in document_chunks]
        metadatas = [{'page_number': chunk['page_number']} for chunk in document_chunks]
        
        print("Generating embeddings for all chunks... (This may take a moment)")
        embeddings = self.model.encode(texts, show_progress_bar=True).tolist()
        print("Embeddings generated.")
        
        # Add the data to the collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(ids)} documents to the collection.")

    def query(self, user_query: str, num_results: int = 3) -> list[dict]:
        """
        Queries the collection to find the most relevant document chunks.

        Args:
            user_query (str): The user's question or query.
            num_results (int): The number of relevant chunks to return.

        Returns:
            list[dict]: A list of the most relevant document chunks and their metadata.
        """
        print(f"\nQuerying for: '{user_query}'")
        # Generate an embedding for the user's query
        query_embedding = self.model.encode(user_query).tolist()
        
        # Perform the query
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=num_results
        )
        
        # The result is a dictionary, we are interested in documents and metadatas
        return results