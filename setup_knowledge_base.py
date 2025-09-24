# setup_knowledge_base.py

from src.knowledge_base.loader import load_and_chunk_pdf
from src.knowledge_base.vector_store import VectorStoreManager

def main():
    """
    Main function to set up the knowledge base.
    1. Loads and chunks the PDF.
    2. Populates the vector store with the chunks.
    3. Runs a test query.
    """
    print("--- Starting Knowledge Base Setup ---")
    
    # Step 1: Load and chunk the document
    pdf_path = "data/Serri Doc.pdf"
    chunks = load_and_chunk_pdf(pdf_path)
    
    if not chunks:
        print("No chunks were created. Exiting.")
        return
        
    # Step 2: Initialize the vector store and populate it
    vector_store = VectorStoreManager()
    vector_store.populate_collection(chunks)
    
    print("\n--- Knowledge Base Setup Complete ---")
    
    # Step 3: Run a test query to see if it works
    test_query = "What is Serri AI?"
    results = vector_store.query(test_query)
    
    print("\n--- Test Query Results ---")
    if results and results['documents']:
        # ChromaDB returns results in a nested list, so we access the first element
        for i, doc in enumerate(results['documents'][0]):
            print(f"Result {i+1}:")
            print(f"  Metadata: {results['metadatas'][0][i]}")
            print(f"  Text: {doc[:200]}...") # Print first 200 chars
    else:
        print("No results found for the test query.")

if __name__ == "__main__":
    main()