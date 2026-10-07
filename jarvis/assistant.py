import re

from jarvis.commands import CommandHandler
from jarvis.config import settings
from jarvis.llm_client import LLMClient
from jarvis.memory import MemoryManager
from jarvis.reminders import ReminderManager
from jarvis.voice import VoiceEngine


class LuciferAssistant:
    def __init__(self):
        self.name = settings.assistant_name
        self.commands = CommandHandler()
        self.voice = VoiceEngine(self.name)
        self.reminders = ReminderManager(settings.reminder_file)
        self.memory = MemoryManager(settings.memory_file)
        self.llm = LLMClient(api_key=settings.openai_api_key, model=settings.openai_model)

    def run(self):
        print(f"{self.name} is online. Type your command or ask me anything.")
        while True:
            raw = self.voice.listen_for_text_mode()
            if not raw:
                continue
            response = self.process_text(raw)
            print(response)
            if response == "__EXIT__":
                break

    def run_voice(self):
        self.voice.speak(f"{self.name} is listening. Say my name followed by a command.")
        while True:
            raw = self.voice.wait_for_wake_word("lucifer")
            command = raw.replace("lucifer", "", 1).strip()
            if not command:
                self.voice.speak("I am listening.")
                continue
            result = self.process_text(command)
            self.voice.speak(result if result != "__EXIT__" else "Goodbye.")
            if result == "__EXIT__":
                break

    def process_text(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        original = text.strip()
        clean = original.lower().strip()
        clean = clean.replace("lucifer", "", 1).strip()

        if clean in {"exit", "quit", "bye", "goodbye", "shutdown", "stop"}:
            return "__EXIT__"

        self.memory.add_conversation(original)
        self.memory.learn_from_prompt(original)

        command = self.commands.handle(original)

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

            if action == "create_file":
                payload = command["text"]
                parts = payload.split(maxsplit=3)
                if len(parts) < 4:
                    return "Use the format: create file path/to/file.txt with your content"
                file_path = parts[2]
                content = payload.split(" ", 3)[3] if len(payload.split(" ", 3)) >= 4 else ""
                return self.commands.create_file(file_path, content)

            if action == "list_files":
                target = command["text"].replace("list files", "", 1).strip()
                target = target.replace("show files", "", 1).strip()
                target = target.replace("ls", "", 1).strip()
                return self.commands.list_files(target or ".")

            if action == "focus_mode":
                return "Focus mode activated. I will help you minimize distractions, prioritize tasks, and keep your workflow smooth."

        if isinstance(command, str):
            return command

        if clean.startswith("remind"):
            parsed = self._extract_reminder(original)
            if parsed:
                return self.reminders.add(parsed["message"], parsed["when"])

        if clean.startswith("list reminders"):
            return self.reminders.list()

        if clean.startswith("memory"):
            return self.memory.get_context() or "I do not have saved memory yet."

        if clean.startswith("voice") or clean.startswith("listen"):
            return self.voice_loop()

        if clean.startswith("open "):
            return self.commands.open_app_or_url(original)

        memory_context = self.memory.get_context()
        if any(word in clean for word in ["debug", "fix", "code", "write", "script", "python", "javascript", "html", "css", "bug", "function", "api", "react", "node"]):
            return self.llm.generate_response(original, mode="code", memory_context=memory_context)

        if any(word in clean for word in ["who are you", "what are you", "what is your name", "hello", "hi", "how are you", "how can you help"]):
            return self.llm.generate_response(original, mode="general", memory_context=memory_context)

        return self.llm.generate_response(original, mode="general", memory_context=memory_context)

    def _extract_reminder(self, text: str):
        match = re.search(
            r"(?:remind(?: me)?(?: to)?\s+)?(.+?)(?:\s+in\s+(\d+)\s*(minute|minutes|hour|hours|day|days)|\s+at\s+(\d{1,2}:\d{2}\s*(?:am|pm)?))",
            text,
            flags=re.I,
        )
        if not match:
            return None

        message = match.group(1).strip()
        if not message:
            message = "Your reminder"

        if match.group(2):
            amount = match.group(2)
            unit = match.group(3)
            when = f"in {amount} {unit}"
        else:
            when = match.group(4) or "in 10 minutes"

        return {"message": message, "when": when}

    def voice_loop(self):
        self.voice.speak("I am listening.")
        while True:
            raw = self.voice.listen_once()
            if not raw:
                continue
            lower = raw.lower().strip()
            if lower in {"exit", "quit", "bye", "goodbye", "shutdown", "stop"}:
                self.voice.speak("Goodbye.")
                return "__EXIT__"
            result = self.process_text(raw)
            self.voice.speak(result if result != "__EXIT__" else "Goodbye.")
            if result == "__EXIT__":
                break
        return "__EXIT__"
