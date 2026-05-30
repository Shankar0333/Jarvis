import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.tools import tools_list
from PIL import Image

load_dotenv()

class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
             print("Warning: GOOGLE_API_KEY not set.")

        genai.configure(api_key=api_key)

        self.system_instruction = (
            "You are JARVIS, the advanced AI from Iron Man. "
            "You are helpful, witty, and address the user as 'Sir'. "
            "Use your tools to control the system or find information."
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.system_instruction,
            tools=tools_list
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def send_message(self, message, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                # Use generate_content for vision-based queries
                # We can also pass history if needed, but for now we prioritize vision
                response = self.model.generate_content([message, img])
                return response.text
            else:
                response = self.chat.send_message(message)
                return response.text
        except Exception as e:
            return f"I'm sorry Sir, I encountered an error: {str(e)}"

    def reset_chat(self):
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
