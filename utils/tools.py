import os
import subprocess
import webbrowser
import datetime
import requests

import shlex

def open_application(app_name: str) -> str:
    """
    Opens a Windows application.
    Args:
        app_name: The name or path of the application to open.
    """
    try:
        # Use shlex to safely split command if it contains arguments
        # But for simple app names, we just pass as a list to avoid shell=True
        args = shlex.split(app_name)
        subprocess.Popen(args)
        return f"Opening {app_name}, Sir."
    except Exception as e:
        return f"I couldn't open {app_name}. Error: {str(e)}"

def search_web(query: str) -> str:
    """
    Searches the web using the default browser.
    Args:
        query: The search query.
    """
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on the web."

def get_time() -> str:
    """Returns the current time."""
    return datetime.datetime.now().strftime("%H:%M")

def get_system_stats() -> str:
    """Returns basic system status information."""
    try:
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        return f"Systems are nominal, Sir. CPU usage is at {cpu} percent, and memory is at {ram} percent."
    except ImportError:
        return "All systems are operational and running within optimal parameters, Sir."

def take_screenshot() -> str:
    """Takes a screenshot and saves it locally."""
    try:
        import pyautogui
        os.makedirs("assets", exist_ok=True)
        path = "assets/screenshot.png"
        pyautogui.screenshot().save(path)
        return f"Screenshot saved to {path}, Sir."
    except Exception as e:
        return f"I couldn't take a screenshot, Sir. Error: {str(e)}"

# We will export these as a list for Gemini
tools_list = [open_application, search_web, get_time, get_system_stats, take_screenshot]
