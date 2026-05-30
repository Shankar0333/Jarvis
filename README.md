# JARVIS - Advanced AI System

A full-featured JARVIS-style AI assistant for Windows, powered by Google Gemini.

## Features
- **Tony Stark Experience**: Biometric identity scanning on startup and a British-voiced AI persona.
- **Autonomous Agent**: Jarvis can sequence multiple tools to solve complex goals (e.g., "Research X and write a report").
- **Futuristic HUD**: Animated Arc Reactor, real-time CPU/RAM bars, and a scrolling system log terminal.
- **Advanced Vision**: Screen capture and multimodal analysis to "see" your work.
- **Web Research**: Autonomous scraping and information retrieval from the live web.
- **Python Scripting**: Jarvis can write and execute code locally to process data or automate files.
- **Productivity Suite**: Native support for PDF summarization, Excel analysis, and PowerPoint generation.
- **Hardware Control**: Control system volume, brightness, and manage running processes.
- **Memory & Scheduling**: Persistent local memory for reminders and user facts.

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
