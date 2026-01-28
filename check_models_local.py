import google.generativeai as genai
import os
from dotenv import load_dotenv

print("Starting diagnostic...")
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

log_lines = []

if not api_key:
    msg = "ERROR: No API Key found in .env file."
    print(msg)
    log_lines.append(msg)
else:
    msg = f"API Key found (starts with: {api_key[:8]}...)"
    print(msg)
    log_lines.append(msg)
    
    genai.configure(api_key=api_key)
    
    try:
        print("Listing models...")
        models = list(genai.list_models())
        log_lines.append(f"Total models found: {len(models)}")
        for m in models:
            line = f"Model: {m.name} | Methods: {m.supported_generation_methods}"
            print(line)
            log_lines.append(line)
            
        # Try a quick test generation with gemini-pro if available, else first available
        log_lines.append("\n--- Connection Test ---")
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Test")
            log_lines.append(f"gemini-pro test: Success")
        except Exception as e:
            log_lines.append(f"gemini-pro test: Failed ({e})")
            
    except Exception as e:
        log_lines.append(f"CRITICAL ERROR listing models: {e}")

with open("model_debug_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print("Diagnostic complete. Results saved to model_debug_log.txt")
