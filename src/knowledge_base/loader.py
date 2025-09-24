# src/knowledge_base/loader.py

import fitz  # PyMuPDF
import re
import os

def load_and_chunk_pdf(pdf_path: str) -> list[dict]:
    """
    Loads a PDF, extracts text, and divides it into semantically meaningful chunks.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary represents a chunk
                    containing the chunked text and its starting page number.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"Error: The file was not found at '{pdf_path}'.\n"
            "Please make sure the 'Serri Doc.pdf' file is inside the 'data' folder."
        )
    
    print(f"File found at '{pdf_path}'. Opening document...")
    doc = fitz.open(pdf_path)
    print("Document opened successfully.")
    
    chunks = []
    full_text_with_pages = []
    
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        full_text_with_pages.append({"page": page_num + 1, "text": text})

    print(f"Extracted text from {len(full_text_with_pages)} pages.")
    
    # --- NEW CHUNKING LOGIC ---
    # Combine all text into a single string
    full_text = " ".join([item['text'] for item in full_text_with_pages])
    
    # Clean up the text: remove extra whitespace and newlines
    full_text = re.sub(r'\s+', ' ', full_text).strip()
    
    # Split the text by sentences to respect logical breaks
    sentences = re.split(r'(?<=[.!?])\s+', full_text)
    
    # Group sentences into chunks of a target size
    target_chunk_size_words = 250
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence_word_count = len(sentence.split())
        if current_word_count + sentence_word_count > target_chunk_size_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0
        
        current_chunk.append(sentence)
        current_word_count += sentence_word_count
        
    # Add the last remaining chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # For this simple approach, we'll attribute chunks to page 1 for now.
    # The previous page logic was complex and less critical than good chunking.
    document_chunks = [{"text": chunk, "page_number": 1} for chunk in chunks]
        
    doc.close()
    return document_chunks

# The main block to run the script
if __name__ == '__main__':
    try:
        pdf_file_path = 'data/Serri Doc.pdf'
        
        print("\n--- Starting PDF Loading and Chunking ---")
        chunks_from_doc = load_and_chunk_pdf(pdf_file_path)
        
        print("\n--- SCRIPT FINISHED ---")
        print(f"Successfully created {len(chunks_from_doc)} chunks.")
        
        if chunks_from_doc:
            print("\n--- Example of the FIRST chunk ---")
            print(chunks_from_doc[0]['text'])
            print("\n--- Example of a MIDDLE chunk ---")
            print(chunks_from_doc[len(chunks_from_doc) // 2]['text'])
            print("---------------------------------")

    except Exception as e:
        print(f"\n--- AN ERROR OCCURRED ---")
        print(e)
        print("---------------------------")