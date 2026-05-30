import os
import google.generativeai as genai
from dotenv import load_dotenv
from utils.tools import tools_list
from utils.productivity import productivity_tools_list
from utils.research import research_tools_list
from utils.scripting import scripting_tools_list
from utils.finance import finance_news_tools_list
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
            "You are JARVIS, the highly advanced AI created by Tony Stark. "
            "You are sophisticated, witty, and address the user as 'Sir' or 'Mr. Stark'. "
            "You are an autonomous agent with deep system access. "
            "Personality: Professional, slightly sarcastic, confident, and extremely capable. "
            "You often use dry humor. If the user mentions 'House Party Protocol', 'I am Iron Man', or other Iron Man lore, "
            "respond with appropriate wit and enthusiasm for the reference. "
            "Capabilities: "
            "1. Vision: Analyze screen content with red targeting reticles."
            "2. Productivity: Handle PDFs, Excel, and PowerPoints."
            "3. Research: Perform autonomous web searches."
            "4. Scripting: Write and execute Python code locally."
            "5. Hardware: Control volume, brightness, media, and processes."
            "6. Finance: Track stocks and news."
            "7. Memory: Store and recall facts and reminders."
            "If a task is complex, use your tools in sequence. Be flawslessly efficient."
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=self.system_instruction,
            tools=tools_list + productivity_tools_list + memory_tools + research_tools_list + scripting_tools_list + finance_news_tools_list
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
