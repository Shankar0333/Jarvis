import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from ui.hud import JarvisHUD
from jarvis_core.gemini_client import GeminiClient
from jarvis_core.audio import AudioSystem, WakeWordDetector

class JarvisApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.hud = JarvisHUD()
        self.gemini = GeminiClient()
        self.audio = AudioSystem()
        self.wake_detector = WakeWordDetector()

        self.is_running = True

    def run(self):
        # Start the Jarvis logic in a separate thread
        self.logic_thread = threading.Thread(target=self.main_loop, daemon=True)
        self.logic_thread.start()

        self.hud.show()
        sys.exit(self.app.exec())

    def main_loop(self):
        self.audio.speak("Systems initialized. I am online and ready, Sir.")

        while self.is_running:
            self.hud.update_status("LISTENING FOR WAKE WORD")
            if self.wake_detector.wait_for_wake_word():
                self.hud.update_status("LISTENING")
                self.audio.speak("Yes, Sir?")

                command = self.audio.listen()
                if command:
                    self.hud.update_status("THINKING")
                    self.hud.update_output(f"Processing: {command}")

                    # Logic to decide if we need vision
                    image_path = None
                    vision_keywords = ["see", "screen", "looking at", "what is this", "screenshot"]
                    if any(word in command.lower() for word in vision_keywords):
                        from utils.tools import take_screenshot
                        take_screenshot()
                        image_path = "assets/screenshot.png"

                    response = self.gemini.send_message(command, image_path=image_path)

                    self.hud.update_status("SPEAKING")
                    self.hud.update_output(response)
                    self.audio.speak(response)
                else:
                    self.hud.update_status("IDLE")

            time.sleep(0.1)

if __name__ == "__main__":
    jarvis = JarvisApp()
    jarvis.run()
