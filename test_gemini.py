import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="Reply with Hello World"
    )

    print("Gemini response:")
    print(response.text)

except Exception as error:
    print(f"Gemini request failed: {type(error).__name__}")
    print(error)