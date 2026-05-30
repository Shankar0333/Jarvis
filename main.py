import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from ui.hud import JarvisHUD, BiometricSplash
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
        # Show splash first
        self.splash = BiometricSplash(self.on_authenticated)
        self.splash.show()
        sys.exit(self.app.exec())

    def on_authenticated(self):
        # Start the Jarvis logic in a separate thread
        self.logic_thread = threading.Thread(target=self.main_loop, daemon=True)
        self.logic_thread.start()

        # Start proactive monitor thread
        self.monitor_thread = threading.Thread(target=self.proactive_monitor, daemon=True)
        self.monitor_thread.start()

        self.hud.show()

    def proactive_monitor(self):
        """Monitors system and reminders to speak proactively."""
        last_remind_check = 0
        while self.is_running:
            now = time.time()

            # Check reminders every 60 seconds
            if now - last_remind_check > 60:
                from jarvis_core.memory import memory_manager
                reminders = memory_manager.get_reminders()
                if "no pending reminders" not in reminders.lower():
                    self.hud.add_log("PROACTIVE ALERT: Reminder due.")
                    # In a real app, check specific time. For now, just log.
                last_remind_check = now

            # Monitor battery/CPU
            import psutil
            if psutil.cpu_percent() > 90:
                 self.hud.add_log("WARNING: CPU load critical.")

            time.sleep(10)

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
