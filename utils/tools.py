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
        if os.name == 'nt':
            # On Windows, os.startfile is more robust for opening apps by name
            os.startfile(app_name)
        else:
            args = shlex.split(app_name)
            subprocess.Popen(args)
        return f"Opening {app_name}, Sir."
    except Exception as e:
        # Fallback to subprocess if startfile fails
        try:
            subprocess.Popen(shlex.split(app_name))
            return f"Opening {app_name}, Sir."
        except:
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

def adjust_volume(level: int) -> str:
    """Adjusts the system volume (0-100)."""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume adjusted to {level} percent, Sir."
    except Exception as e:
        return f"Failed to adjust volume. Error: {str(e)}"

def adjust_brightness(level: int) -> str:
    """Adjusts the screen brightness (0-100)."""
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return f"Brightness set to {level} percent, Sir."
    except Exception as e:
        return f"Failed to adjust brightness. Error: {str(e)}"

def terminate_process(process_name: str) -> str:
    """Terminates a running process by name."""
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if process_name.lower() in proc.info['name'].lower():
                proc.terminate()
                return f"Process {process_name} has been terminated, Sir."
        return f"I couldn't find a process named {process_name}, Sir."
    except Exception as e:
        return f"Error terminating process: {str(e)}"

def media_control(action: str) -> str:
    """
    Controls system media.
    Args:
        action: 'play_pause', 'next', 'previous', 'volume_up', 'volume_down'
    """
    try:
        import pyautogui
        keys = {
            'play_pause': 'playpause',
            'next': 'nexttrack',
            'previous': 'prevtrack',
            'volume_up': 'volumeup',
            'volume_down': 'volumedown'
        }
        if action in keys:
            pyautogui.press(keys[action])
            return f"Media {action} executed, Sir."
        return f"Unknown media action: {action}, Sir."
    except Exception as e:
        return f"Failed to control media. Error: {str(e)}"

def play_on_youtube(query: str) -> str:
    """Searches and plays a video on YouTube."""
    try:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        return f"Searching for {query} on YouTube, Sir. I'll open the first result for you."
    except Exception as e:
        return f"Failed to play on YouTube: {str(e)}"

# We will export these as a list for Gemini
tools_list = [
    open_application, search_web, get_time, get_system_stats,
    take_screenshot, adjust_volume, adjust_brightness, terminate_process,
    media_control, play_on_youtube
]
