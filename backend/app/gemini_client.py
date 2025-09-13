import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def rate_developer(self, developer_data: dict, query: str) -> dict:
        prompt = f"""
        As an expert AI talent scout for software engineers, your task is to evaluate a developer's profile based on the provided data. The user is searching for: "{query}".

        Analyze the following developer data:
        {json.dumps(developer_data, indent=2)}

        Based on the data, provide a "cracked_score" from 1 to 100, where 100 is a perfect match for a "cracked" developer according to the user's query. Also, provide a short "reasoning" for your score.

        A "cracked" developer is someone who is exceptionally skilled, innovative, and productive. Consider factors like code quality, project complexity, innovation, and community impact.

        Return the output as a JSON object with two keys: "cracked_score" and "reasoning".
        """
        try:
            response = self.model.generate_content(prompt)
            # It's possible the model doesn't return perfect JSON, so we need to find it
            json_response_str = response.text.strip().replace('`', '').replace('json', '')
            return json.loads(json_response_str)
        except Exception as e:
            print(f"Error generating rating for developer: {e}")
            return {"cracked_score": 0, "reasoning": "Error analyzing profile."}

