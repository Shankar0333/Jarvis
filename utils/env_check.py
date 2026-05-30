import os
from dotenv import load_dotenv

def check_env():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("Error: Please set your GOOGLE_API_KEY in the .env file.")
        return False
    return True

if __name__ == "__main__":
    if check_env():
        print("Environment check passed.")
    else:
        print("Environment check failed.")
