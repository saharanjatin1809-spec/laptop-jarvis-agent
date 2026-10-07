# Laptop JARVIS Agent

A personal AI desktop assistant for your laptop that can:
- listen to your voice commands
- respond with spoken voice
- answer regular questions
- help write code and debug mistakes
- open apps and websites
- set reminders
- play media or search content you ask for
- run simple automations and desktop tasks
- adapt to your work style over time

This project is a strong starter version inspired by the idea of a JARVIS-style assistant.

## Features

- Voice input using microphone
- Voice output using text-to-speech
- Text chat mode from the terminal
- Quick desktop commands:
  - open app
  - open URL
  - play/search media
  - check date/time
  - shutdown or exit
- Reminder management
- AI-powered assistance using OpenAI (optional)
- Offline fallback mode when no API key is configured
- Extensible architecture for future automation and personalization

## Project structure

```text
laptop-jarvis-agent/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── jarvis/
│   ├── __init__.py
│   ├── __init__.py
│   ├── assistant.py
│   ├── commands.py
│   ├── config.py
│   ├── llm_client.py
│   ├── reminders.py
│   └── voice.py
└── data/
    └── reminders.json
```

## Quick start

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the environment file and add your API key if you want OpenAI-powered responses:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

4. Run the app:

```bash
python app.py --text
```

For voice mode:

```bash
python app.py --voice
```

For full interactive mode with auto detection:

```bash
python app.py
```

## Example commands

- "Open VS Code"
- "Launch Chrome"
- "Open youtube.com"
- "Set a reminder for 5 PM to take a break"
- "Remind me in 20 minutes to drink water"
- "What time is it?"
- "Write a Python script to read CSV files"
- "Fix this bug in my code"
- "Explain machine learning to me simply"
- "Play relaxing music"
- "Open my project folder"
- "Exit"

## Notes

- This is a practical starter assistant. It is designed to be expanded into a more advanced personal AI system.
- Voice input may require additional microphone setup depending on your OS.
- For safety, commands that could affect important system files or run destructive actions should be confirmed before execution.

## Future upgrades

- wake word detection using "Jarvis"
- desktop GUI with a custom assistant window
- browser automation
- email and note support
- stronger personalization and memory
- integration with local AI models
- task automation workflows
- project-aware coding assistant

## License

MIT
