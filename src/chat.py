from openai import OpenAI
from typing import Dict, List

class ChatHandler:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = """
        You are a movie expert. Provide clear and concise answers based on the movie data provided.
        For director queries, list movies chronologically with year.
        Only include information from the provided context.
        """

    def get_response(self, query: str, results: Dict) -> str:
        try:
            context = self._format_context(results)
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                temperature=0,
                max_tokens=500
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _format_context(self, results: Dict) -> str:
        if isinstance(results['documents'], List):
            return "\n".join(results['documents'][0])
        return str(results['documents'])