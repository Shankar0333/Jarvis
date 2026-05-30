# JARVIS - Advanced AI System

A full-featured JARVIS-style AI assistant for Windows, powered by Google Gemini.

## Features
- **Voice Interaction**: Sophisticated British voice with wake-word detection ("Jarvis").
- **Futuristic HUD**: Semi-transparent PyQt6 overlay.
- **Multilingual Support**: Powered by Google Speech Recognition and Gemini.
- **System Integration**: Open apps, search the web, get system stats.
- **Vision**: Jarvis can take screenshots and "see" what you are looking at.
- **Advanced AI**: Integrated with Gemini 1.5 Flash for witty, helpful, and high-context interactions.

## Prerequisites
- Windows OS (recommended)
- Python 3.10+
- PortAudio (for audio recording)
- Google Gemini API Key

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` and add your `GOOGLE_API_KEY`.
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
- Say "Jarvis" to wake the system.
- Ask questions, command system actions, or ask Jarvis to search the web.
- Try: "Jarvis, open Notepad," or "Jarvis, what's on my screen?"
