import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path


class CommandHandler:
    def __init__(self):
        self.app_map = {
            "vscode": "code",
            "visual studio code": "code",
            "code": "code",
            "chrome": "google-chrome",
            "browser": "google-chrome",
            "firefox": "firefox",
            "terminal": "gnome-terminal",
            "cmd": "cmd",
            "notepad": "notepad",
            "calculator": "calc",
            "spotify": "spotify",
            "discord": "discord",
            "slack": "slack",
            "file explorer": "explorer",
            "explorer": "explorer",
            "sublime": "sublime_text",
            "sublime text": "sublime_text",
            "cursor": "cursor",
            "pycharm": "pycharm",
            "idea": "idea",
            "vscode code": "code",
        }

    def handle(self, text: str):
        if not text:
            return None

        lower = text.lower().strip()
        lower = lower.replace("lucifer", "", 1).strip()

        if lower in {"exit", "quit", "bye", "goodbye", "shutdown", "stop"}:
            return "__EXIT__"

        if lower.startswith("open ") or lower.startswith("launch "):
            return self.open_app_or_url(text)

        if lower.startswith("search "):
            return {"type": "search", "text": text}

        if "remind" in lower or "reminder" in lower or "alarm" in lower:
            return {"type": "reminder", "text": text}

        if lower.startswith("play "):
            return {"type": "play", "text": text}

        if "time" in lower:
            return {"type": "time", "text": text}

        if "date" in lower:
            return {"type": "date", "text": text}

        if "folder" in lower or "directory" in lower:
            return {"type": "folder", "text": text}

        if lower.startswith("create file ") or lower.startswith("make file "):
            return {"type": "create_file", "text": text}

        if lower.startswith("list files") or lower.startswith("show files") or lower.startswith("ls "):
            return {"type": "list_files", "text": text}

        if lower.startswith("focus mode"):
            return {"type": "focus_mode", "text": text}

        return None

    def open_app_or_url(self, text: str):
        command = text.strip()
        lower = command.lower()
        lower = lower.replace("lucifer", "", 1).strip()

        if re.search(r"https?://|www\.", command):
            webbrowser.open(command)
            return "Opened the link you requested."

        app_name = command.split(maxsplit=1)[1].strip().strip("\"'") if " " in command else ""
        if not app_name:
            return "Which app or website should I open?"

        app = self.app_map.get(app_name.lower(), app_name)

        try:
            if sys.platform.startswith("win"):
                if app in {"explorer", "notepad", "calc", "cmd"}:
                    subprocess.Popen(app, shell=True)
                else:
                    subprocess.Popen(app)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", app])
            else:
                subprocess.Popen(app)
            return f"Opened {app_name}."
        except Exception:
            try:
                webbrowser.open(f"https://www.google.com/search?q={app_name.replace(' ', '+')}")
                return f"I opened a browser search for {app_name}."
            except Exception:
                return f"I could not open {app_name}."

    def open_path(self, path: str):
        try:
            p = Path(path).expanduser()
            if not p.exists():
                return f"The path '{path}' does not exist."
            if sys.platform.startswith("win"):
                os.startfile(str(p))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(p)])
            else:
                subprocess.Popen(["xdg-open", str(p)])
            return f"Opened {path}."
        except Exception:
            return f"I could not open {path}."

    def list_files(self, target: str = "."):
        target_path = Path(target).expanduser()
        if not target_path.exists():
            return f"The path '{target}' does not exist."

        items = sorted([p.name for p in target_path.iterdir()])
        if not items:
            return f"The directory '{target}' is empty."
        return "\n".join(items[:30])

    def create_file(self, path: str, content: str = ""):
        p = Path(path).expanduser()
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Created file at {path}."
        except Exception as exc:
            return f"I could not create the file: {exc}"

    def play_media(self, text: str):
        query = text.replace("play", "", 1).strip()
        if not query:
            return "What should I play?"
        webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
        return f"Searching YouTube for {query}."

    def search_web(self, text: str):
        query = text.replace("search", "", 1).strip()
        if not query:
            return "What should I search for?"
        webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        return f"Searching the web for {query}."

    @staticmethod
    def current_time():
        return datetime.now().strftime("%I:%M %p")

    @staticmethod
    def current_date():
        return datetime.now().strftime("%A, %B %d, %Y")
