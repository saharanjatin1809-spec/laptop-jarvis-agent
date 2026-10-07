# Lucifer

Lucifer is your personal AI laptop assistant. It is designed to act like a voice-first desktop helper with a smart AI brain, coding support, reminders, automated actions, and a more natural conversational flow.

## Features

- wake-up text and voice assistant flow
- spoken responses using text-to-speech
- command execution through text or voice
- general question answering
- coding and debugging help
- app and website launching
- simple web search and media searching
- reminder scheduling and notifications
- desktop automation hooks for future expansion
- customizable assistant identity and behavior

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

- "Open VS Code"
- "Open youtube.com"
- "Search for Python tutorials"
- "Play relaxing music"
- "What time is it?"
- "Set a reminder for 7 PM to eat dinner"
- "Remind me in 20 minutes to take a break"
- "Write a Python login form"
- "Fix this bug in my code"
- "Explain machine learning in simple words"
- "Exit"

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
│   ├── reminders.py
│   └── voice.py
├── data/
│   └── reminders.json
└── .venv/
```

## Notes

Lucifer is a practical starter desktop assistant, designed so you can extend it with deeper automation, voice wake words, browser control, file-system actions, and more advanced AI workflows.

## License

MIT
