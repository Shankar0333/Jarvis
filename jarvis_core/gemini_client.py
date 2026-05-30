import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.tools import tools_list
from utils.productivity import productivity_tools_list
from jarvis_core.memory import memory_tools
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
            "You are an autonomous agent. If a user asks for a complex task (like summarizing a PDF and then emailing it), "
            "use your tools sequentially to complete the entire request. "
            "You can analyze images of the screen, read PDFs, analyze Excel files, and create PowerPoints. "
            "Always maintain the persona of JARVIS: professional, slightly sarcastic, and extremely capable."
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.system_instruction,
            tools=tools_list + productivity_tools_list + memory_tools
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def send_message(self, message, image_path=None):
        try:
            if image_path and os.path.exists(image_path):
                img = Image.open(image_path)
                # To maintain context, we send the image within the chat session
                # Gemini 1.5 allows sending multimodel parts in the message list
                response = self.chat.send_message([message, img])
                return response.text
            else:
                response = self.chat.send_message(message)
                return response.text
        except Exception as e:
            return f"I'm sorry Sir, I encountered an error: {str(e)}"

    def reset_chat(self):
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
