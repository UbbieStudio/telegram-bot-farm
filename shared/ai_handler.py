import os
import httpx
from dotenv import load_dotenv
from shared.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class AIHandler:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Switching default to 2.5 Flash because 3.0 Pro is pay-only for API keys
        self.current_model = "gemini-2.5-flash"

    def set_model(self, model_name: str):
        self.current_model = model_name

    async def get_gemini_response(self, prompt: str):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.current_model}:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                result = response.json()
                
                if response.status_code == 200:
                    return result['candidates'][0]['content']['parts'][0]['text']
                else:
                    error_msg = result.get('error', {}).get('message', 'Unknown Error')
                    # Custom help message for the 429 error
                    if response.status_code == 429:
                        return f"❌ Quota Error: {self.current_model} is likely pay-only. Use /mode to switch to Gemini 2.5 Flash!"
                    return f"Gemini Error ({response.status_code}): {error_msg}"
        except Exception as e:
            logger.error(f"Request Error: {e}")
            return "Connection Error. The AI is currently unavailable."

    async def ask(self, prompt: str, provider: str = "openai"):
        return await self.get_gemini_response(prompt)