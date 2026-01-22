from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API KEY FOUND:", bool(api_key))

client = genai.Client(api_key=api_key)

models = client.models.list()

print("\nAVAILABLE MODELS:\n")

for model in models:
    print(model.name)
