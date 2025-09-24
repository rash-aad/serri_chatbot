# Serri AI Lead Generation Chatbot

## 📄 Description

This project is a fully functional, conversational AI chatbot built to simulate a real-world business requirement. Based on a detailed product specification for a fictional company, "Serri AI," this bot acts as an interactive landing page designed to inform visitors, qualify leads, and schedule demos.

The application features a hybrid conversational system, combining a structured, stateful flow for lead qualification with a powerful, open-ended Q&A capability powered by a Retrieval-Augmented Generation (RAG) pipeline.

## ✨ Features

* **Stateful Conversation Management:** Guides users through a multi-step lead qualification process, asking about their industry, company size, and needs.
* **RAG-Powered Q&A:** Answers open-ended questions by retrieving relevant information from a 38-page PDF document.
    * **Retrieval:** Uses `sentence-transformers` to create vector embeddings from the document, stored in a `ChromaDB` vector database for fast semantic search.
    * **Generation:** Leverages the **Cohere API** to generate natural, human-like answers based on the retrieved context.
* **Hybrid Logic:** Intelligently routes the user between the structured qualification flow and the open-ended Q&A mode based on their choices.
* **Interactive Front End:** A clean, modern chat interface built with HTML, CSS, and JavaScript.
* **API-based Architecture:** The entire application is powered by a Python **Flask** server, making it robust and scalable.

## ⚙️ Setup and Installation

Follow these steps to set up and run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd serri_chatbot
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    * Create a file named `.env` in the root of the project folder.
    * Add your Cohere API key to this file:
        ```
        COHERE_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Build the Knowledge Base:**
    * Before running the main app, you must process the PDF and build the vector database. Run the setup script from your terminal:
        ```bash
        python setup_knowledge_base.py
        ```
    * This will create a `chroma_db` folder in your project directory containing the knowledge base.

## ▶️ How to Run

After completing the setup, run the Flask web application:

```bash
flask --app app run --port 5001
# serri_chatbot
