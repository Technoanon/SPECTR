"""
xAI Client for SPECTR
Simple wrapper to call Grok API with the tactical prompt.
"""
import os
import requests
from typing import List, Dict
from dotenv import load_dotenv

# Force load .env at import time
load_dotenv()

class XAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found. Check your .env file in the project root.")
       
        self.base_url = "https://api.x.ai/v1/chat/completions"
        self.model = "grok-3"

    def chat(self, messages: List[Dict], temperature: float = 0.3, max_tokens: int = 2048):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[API Error]: {str(e)}"


# Quick test when running directly
if __name__ == "__main__":
    print("xAI Client ready.")
    print("Key loaded:", "YES" if os.getenv("XAI_API_KEY") else "NO")
