"""
Quick script to check available Gemini models and test connection.
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\n📋 Available Gemini Models:")
print("=" * 60)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display: {model.display_name}")
            print(f"   Description: {model.description[:80]}...")
            print()
except Exception as e:
    print(f"❌ Error listing models: {e}")

print("\n🧪 Testing model names with LangChain:")
print("=" * 60)

from langchain_google_genai import ChatGoogleGenerativeAI

test_models = [
    "gemini-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "models/gemini-pro",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash"
]

for model_name in test_models:
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=0.1
        )
        # Try a simple invoke
        response = llm.invoke("Say 'OK'")
        print(f"✅ {model_name} - WORKS!")
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            print(f"❌ {model_name} - 404 Not Found")
        else:
            print(f"❌ {model_name} - {error_msg[:50]}")
