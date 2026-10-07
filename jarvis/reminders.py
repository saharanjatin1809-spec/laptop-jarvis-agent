import json
import re
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path


class ReminderManager:
    def __init__(self, storage_path: str = "data/reminders.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.reminders = self._load()
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._watch, daemon=True)
        self._thread.start()

    def add(self, message: str, when_text: str):
        parsed = self._parse_when(when_text)
        if parsed is None:
            return "I could not understand when to remind you. Try: 'in 20 minutes' or 'at 5 PM'."

        reminder = {
            "message": message,
            "when": when_text,
            "scheduled_at": parsed.isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        with self._lock:
            self.reminders.append(reminder)
            self._save()
        return f"Reminder set: {message} at {when_text}."

    def list(self):
        if not self.reminders:
            return "You do not have any reminders set."
        lines = ["Your reminders:"]
        for reminder in self.reminders:
            lines.append(f"- {reminder['message']} | {reminder['when']}")
        return "\n".join(lines)

    def _parse_when(self, when_text: str):
        text = when_text.lower().strip()

        if "in " in text:
            match = re.search(r"in\s+(\d+)\s*(minute|minutes|hour|hours|day|days)", text)
            if match:
                value = int(match.group(1))
                unit = match.group(2)
                if unit.startswith("minute"):
                    delta = timedelta(minutes=value)
                elif unit.startswith("hour"):
                    delta = timedelta(hours=value)
                elif unit.startswith("day"):
                    delta = timedelta(days=value)
                else:
                    delta = None
                if delta is not None:
                    return datetime.now() + delta

        time_match = re.search(r"(\d{1,2}):(\d{2})\s*(am|pm)?", text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            period = time_match.group(3)
            if period == "pm" and hour < 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0
            scheduled = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            if scheduled < datetime.now():
                scheduled += timedelta(days=1)
            return scheduled

        return None

    def _load(self):
        if not self.storage_path.exists():
            return []
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save(self):
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self.reminders, f, indent=2)

    def _watch(self):
        while not self._stop_event.is_set():
            now = datetime.now()
            with self._lock:
                remaining = []
                for reminder in self.reminders:
                    scheduled = datetime.fromisoformat(reminder["scheduled_at"])
                    if scheduled <= now:
                        print(f"Reminder: {reminder['message']}")
                    else:
                        remaining.append(reminder)
                self.reminders = remaining
                if self.reminders != remaining:
                    self._save()
            time.sleep(10)

    def stop(self):
        self._stop_event.set()
