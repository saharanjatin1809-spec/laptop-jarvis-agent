# Lucifer

Lucifer is your advanced personal AI laptop assistant. It is designed as a more capable desktop helper with voice-first interaction, coding support, reminders, file access, web actions, and personalized memory.

## Features

- wake-word style voice flow
- spoken responses using text-to-speech
- text command interaction
- conversational memory for user preferences
- coding and debugging assistance
- app and website launching
- file listing and file creation helpers
- reminder scheduling and notifications
- web searches and media lookups
- desktop automation-friendly architecture

## Quick start

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create an environment file:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
ASSISTANT_NAME=Lucifer
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
MEMORY_FILE=data/memory.json
REMINDER_FILE=data/reminders.json
```

4. Run the assistant:

Text mode:

```bash
python app.py --text
```

Voice mode:

```bash
python app.py --voice
```

## Example commands

- "Lucifer, open VS Code"
- "Lucifer, open youtube.com"
- "Lucifer, search for Python tutorials"
- "Lucifer, play relaxing music"
- "Lucifer, what time is it?"
- "Lucifer, remind me in 20 minutes to take a break"
- "Lucifer, write a Python login form"
- "Lucifer, fix this bug in my code"
- "Lucifer, create file notes/todo.txt Hello from Lucifer"
- "Lucifer, list files in this directory"
- "Lucifer, remember that I prefer dark mode"
- "Lucifer, what do you remember?"
- "Lucifer, exit"

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
│   ├── assistant.py
│   ├── commands.py
│   ├── config.py
│   ├── llm_client.py
│   ├── memory.py
│   ├── reminders.py
│   └── voice.py
├── data/
│   ├── memory.json
│   └── reminders.json
└── .venv/
```

## Notes

Lucifer is a powerful personal workstation assistant designed for practical use. It is intentionally built to be expandable with more sophisticated automation, deeper desktop control, and richer user personalization.

## License

MIT
