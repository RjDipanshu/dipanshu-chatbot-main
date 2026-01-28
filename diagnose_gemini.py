import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

print("--- Starting Diagnostic ---")
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("ERROR: GOOGLE_API_KEY not found.")
else:
    print("API Key found (length check matches expected format).")
    genai.configure(api_key=api_key)

    print("Attempting to list models...")
    try:
        # Simple list loop
        count = 0
        for m in genai.list_models():
            count += 1
            if 'generateContent' in m.supported_generation_methods:
                print(f"AVAILABLE: {m.name}")
        if count == 0:
            print("No models found! (Possible API Key scope issue?)")
    except Exception as e:
        print(f"CRITICAL ERROR listing models: {e}")

print("--- End Diagnostic ---")
