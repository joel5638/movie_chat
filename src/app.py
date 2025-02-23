import streamlit as st
import os
import pandas as pd
from typing import Tuple, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

from vector_store import MovieVectorStore
from chat import ChatHandler

def init_components() -> Tuple[Optional[MovieVectorStore], Optional[ChatHandler]]:
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            st.error('OpenAI API key not found')
            return None, None

        # Get the correct path to the CSV file
        current_dir = Path(__file__).parent
        csv_path = current_dir.parent / 'data' / 'imdb_top_1000.csv'
        
        df = pd.read_csv(str(csv_path))
        vector_store = MovieVectorStore(api_key)
        vector_store.add_movies(df)
        chat_handler = ChatHandler(api_key)
        
        return vector_store, chat_handler
        
    except Exception as e:
        st.error(str(e))
        return None, None

def main():
    st.title('Movie Assistant')
    
    if 'initialized' not in st.session_state:
        vector_store, chat_handler = init_components()
        if vector_store and chat_handler:
            st.session_state.vector_store = vector_store
            st.session_state.chat_handler = chat_handler
            st.session_state.initialized = True
            st.rerun()
        return

    with st.sidebar:
        st.markdown("""
        **Example Questions**
        - List movies by Christopher Nolan
        - Show top rated movies from 2020
        - Find horror movies rated above 8
        - All sci-fi movies by Spielberg
        """)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Enter your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            results = st.session_state.vector_store.search(prompt)
            response = st.session_state.chat_handler.get_response(prompt, results)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()