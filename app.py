# app.py (for Serri Chatbot)

import os
import cohere
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template # Import render_template

from src.knowledge_base.vector_store import VectorStoreManager
from src.conversation.state_manager import ConversationManager

# --- INITIALIZATION ---
load_dotenv()
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise ValueError("COHERE_API_KEY not found. Please set it in your .env file.")

co = cohere.Client(api_key)
vector_store = VectorStoreManager()
conversation_manager = ConversationManager()
user_sessions = {}
app = Flask(__name__)
print("All components initialized successfully.")


# --- NEW ROUTE TO SERVE THE FRONT END ---
@app.route('/')
def home():
    """Serves the front-end HTML page."""
    return render_template('index.html')


# --- API ENDPOINT ---
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    user_message = data.get('message')

    if not user_id or not user_message:
        return jsonify({"error": "Request must include 'user_id' and 'message'."}), 400

    session = user_sessions.get(user_id, {'state': 'START', 'data': {}})
    current_state = session.get('state', 'START')
    
    if current_state == 'GENERAL_QA':
        print(f"User '{user_id}' is in Q&A mode. Querying knowledge base...")
        retrieved_results = vector_store.query(user_message, num_results=5)
        documents_for_rag = [
            {"title": f"Page {m['page_number']}", "snippet": t}
            for m, t in zip(retrieved_results['metadatas'][0], retrieved_results['documents'][0])
        ]
        
        try:
            response = co.chat(
                message=user_message,
                documents=documents_for_rag,
                preamble="You are Zen, an AI assistant for Serri AI. Answer the user's question based *only* on the provided documents. If the answer isn't in the documents, say so."
            )
            final_response = response.text
        except Exception as e:
            print(f"Error during Cohere generation: {e}")
            final_response = "Sorry, I'm having a technical issue. Please try again."

        session['response'] = final_response
        session['state'] = 'GENERAL_QA'

    else:
        print(f"User '{user_id}' is in a structured flow. Current state: {current_state}")
        session = conversation_manager.handle_message(session, user_message)
        final_response = session.get('response')

    user_sessions[user_id] = session
    print(f"Updated session for '{user_id}': {session}")
    return jsonify({"response": final_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)