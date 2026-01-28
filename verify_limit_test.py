from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

def test_model(model_name):
    print(f"Testing model: {model_name}")
    try:
        llm = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
        response = llm.invoke("Hello, simple test.")
        print(f"Success! Response: {response.content}")
        return True
    except Exception as e:
        print(f"Failed with error: {e}")
        return False

# Test the confirmed available model
test_model("gemini-flash-latest")
