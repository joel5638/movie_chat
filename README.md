# Movie Chat Assistant

A streamlit-based chatbot for movie information using OpenAI and vector search.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/Mac: `source venv/bin/activate`
4. Install dependencies: `pip3 install -r requirements.txt`
5. Add `OPENAI_key` to `.env` in the root directory
6. Run the app: `streamlit run src/app.py`

## Features

- Movie search by director, year, genre, or rating
- Semantic search for movie recommendations
- Chat interface for natural language queries