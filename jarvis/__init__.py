import re
from datetime import datetime

from jarvis.commands import CommandHandler
from jarvis.config import settings
from jarvis.llm_client import LLMClient
from jarvis.reminders import ReminderManager
from jarvis.voice import VoiceEngine


class JarvisAssistant:
    def __init__(self):
        self.commands = CommandHandler()
        self.voice = VoiceEngine()
        self.reminders = ReminderManager(settings.reminder_file)
        self.llm = LLMClient(api_key=settings.openai_api_key, model=settings.openai_model)

    def run(self):
        print("Jarvis is online. Type your command or say something.")
        while True:
            try:
                raw = self.voice.listen_for_text_mode()
            except KeyboardInterrupt:
                print("Goodbye.")
                break

            if raw.strip() == "":
                continue

            response = self.process_text(raw)
            print(response)
            if response == "__EXIT__":
                break

    def process_text(self, text: str) -> str:
        command = self.commands.handle(text)

        if command == "__EXIT__":
            return "__EXIT__"

        if isinstance(command, dict):
            action = command["type"]
            if action == "reminder":
                parsed = self._extract_reminder(command["text"])
                if parsed is None:
                    return "I can set reminders. Example: 'Remind me in 20 minutes to drink water'"
                return self.reminders.add(parsed["message"], parsed["when"])

            if action == "play":
                return self.commands.play_media(command["text"])

            if action == "time":
                return f"The current time is {self.commands.current_time()}."

            if action == "date":
                return f"Today is {self.commands.current_date()}."

            if action == "search":
                return self.commands.search_web(command["text"])

            if action == "folder":
                return self.commands.open_path(".")

        if isinstance(command, str):
            return command

        if text.lower().startswith("remind"):
            parsed = self._extract_reminder(text)
            if parsed:
                return self.reminders.add(parsed["message"], parsed["when"])

        if text.lower().startswith("voice"):
            return self.voice_loop()

        if text.lower().startswith("list reminders"):
            return self.reminders.list()

        if any(word in text.lower() for word in ["debug", "fix", "code", "write", "script", "function", "python", "javascript", "html", "css"]):
            return self.llm.generate_response(text, mode="code")

        return self.llm.generate_response(text, mode="general")

    def _extract_reminder(self, text: str):
        match = re.search(r"(?:remind(?: me)?(?: to)?\s+)?(.+?)(?:\s+in\s+(\d+)\s*(minute|minutes|hour|hours|day|days)|\s+at\s+(\d{1,2}:\d{2}\s*(?:am|pm)?))", text, flags=re.I)
        if not match:
            return None

        message = match.group(1).strip(" ")
        if not message:
            message = "Your reminder"

        when = None
        if match.group(2):
            amount = match.group(2)
            unit = match.group(3)
            when = f"in {amount} {unit}"
        else:
            when = match.group(4) or "in 10 minutes"

        return {"message": message, "when": when}

    def voice_loop(self):
        self.voice.speak("Jarvis is listening.")
        while True:
            raw = self.voice.listen_once()
            if not raw:
                continue
            lower = raw.lower()
            if lower in {"exit", "quit", "goodbye", "bye"}:
                self.voice.speak("Shutting down.")
                return "__EXIT__"
            result = self.process_text(raw)
            self.voice.speak(result if result != "__EXIT__" else "Goodbye.")
            if result == "__EXIT__":
                break
        return "__EXIT__"

    def run_voice(self):
        while True:
            result = self.voice_loop()
            if result == "__EXIT__":
                break
