import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    assistant_name: str = os.getenv("ASSISTANT_NAME", "Lucifer")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    reminder_file: str = os.getenv("REMINDER_FILE", "data/reminders.json")
    memory_file: str = os.getenv("MEMORY_FILE", "data/memory.json")


settings = Settings()
