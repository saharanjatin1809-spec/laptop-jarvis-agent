import json
from pathlib import Path


class MemoryManager:
    def __init__(self, storage_path: str = "data/memory.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        if not self.storage_path.exists():
            return {"preferences": {}, "conversation": []}
        try:
            with self.storage_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("preferences", {})
                    data.setdefault("conversation", [])
                    return data
        except Exception:
            pass
        return {"preferences": {}, "conversation": []}

    def _save(self):
        with self.storage_path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def remember_preference(self, key: str, value: str):
        self.data["preferences"][key.lower()] = value
        self._save()

    def add_conversation(self, text: str):
        if not text:
            return
        self.data.setdefault("conversation", [])
        self.data["conversation"].append(text)
        if len(self.data["conversation"]) > 30:
            self.data["conversation"] = self.data["conversation"][-30:]
        self._save()

    def get_context(self):
        prefs = self.data.get("preferences", {})
        recent = self.data.get("conversation", [])[-8:]
        if not prefs and not recent:
            return ""

        context_lines = []
        if prefs:
            context_lines.append("User preferences:")
            for k, v in prefs.items():
                context_lines.append(f"- {k}: {v}")
        if recent:
            context_lines.append("Recent conversation:")
            for item in recent:
                context_lines.append(f"- {item}")
        return "\n".join(context_lines)

    def learn_from_prompt(self, prompt: str):
        lower = prompt.lower()
        if "remember" in lower and "prefer" in lower:
            for keyword in ["dark mode", "light mode", "python", "javascript", "react", "vscode", "terminal", "music", "focus mode"]:
                if keyword in lower:
                    self.remember_preference("preferred_style", keyword)
                    break
        if "i like" in lower or "i prefer" in lower:
            parts = lower.split("i prefer")
            if len(parts) > 1:
                value = parts[1].strip().strip(".")
                if value:
                    self.remember_preference("preference", value)

    def clear(self):
        self.data = {"preferences": {}, "conversation": []}
        self._save()
