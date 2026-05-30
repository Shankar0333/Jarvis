import pyttsx3
import speech_recognition as sr
import threading
import os

class AudioSystem:
    def __init__(self):
        # Initialize TTS
        self.engine = pyttsx3.init()
        self.set_voice()

        # Initialize STT
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def set_voice(self):
        voices = self.engine.getProperty('voices')
        # Look for a British voice if possible
        british_voice = False
        for voice in voices:
            if "english" in voice.name.lower() and ("uk" in voice.name.lower() or "british" in voice.name.lower()):
                self.engine.setProperty('voice', voice.id)
                british_voice = True
                break

        if not british_voice and voices:
            self.engine.setProperty('voice', voices[0].id)

        self.engine.setProperty('rate', 175) # Slightly slower and more deliberate

    def speak(self, text, lang='en'):
        print(f"JARVIS: {text}")

        # Simple heuristic to switch voice if it looks like a different language
        # or if explicitly passed.
        # For true multilingual, one might need a library like gTTS for better quality
        # but sticking to pyttsx3 for now.

        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"User: {query}")
            return query
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return None

class WakeWordDetector:
    # In a real app, I'd use Porcupine, but for this environment,
    # I'll implement a simple continuous listen for the wake word.
    def __init__(self, wake_word="jarvis"):
        self.wake_word = wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def wait_for_wake_word(self):
        while True:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)
            try:
                query = self.recognizer.recognize_google(audio).lower()
                if self.wake_word in query:
                    return True
            except:
                continue
