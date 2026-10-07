import os
from typing import Optional

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


class LLMClient:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key and OpenAI else None

    def generate_response(self, prompt: str, mode: str = "general", memory_context: str = "") -> str:
        full_prompt = prompt
        if memory_context:
            full_prompt = f"{memory_context}\n\nUser request: {prompt}"

        if self.client is not None:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are Lucifer, a powerful personal AI assistant for a laptop. "
                                "Answer with clarity, practical steps, concise reasoning, and a helpful tone. "
                                "You can help with coding, debugging, productivity, automation, reminders, app control, and general questions."
                            ),
                        },
                        {"role": "user", "content": full_prompt},
                    ],
                    temperature=0.7,
                )
                response = completion.choices[0].message.content
                if response:
                    return response.strip()
            except Exception:
                pass

        return self._offline_response(prompt, mode)

    def _offline_response(self, prompt: str, mode: str = "general") -> str:
        lower = prompt.lower()

        if any(word in lower for word in ["write", "code", "script", "python", "javascript", "html", "css", "bug", "fix", "debug", "function", "api", "react", "node"]):
            return (
                "I can help with that. Define the exact goal, then break it into a small working version. "
                "If you share the code or the error message, I can suggest a fix and explain what is happening step by step."
            )

        if any(word in lower for word in ["open", "launch", "app", "website", "browser", "folder", "directory"]):
            return "I can open apps, websites, and folders for you. Tell me exactly what to open and I will handle it."

        if any(word in lower for word in ["remind", "reminder", "schedule", "alarm"]):
            return "I can set reminders. Try: 'Remind me in 20 minutes to drink water' or 'Set a reminder for 7 PM for my meeting'."

        if any(word in lower for word in ["play", "music", "song", "video", "youtube"]):
            return "I can help you search for media. Tell me the song, artist, or video you want and I will look it up."

        if any(word in lower for word in ["who are you", "what are you", "what is your name"]):
            return "I am Lucifer, your personal laptop AI assistant. I can help with coding, tasks, reminders, questions, and desktop automation."

        return (
            "I am Lucifer, your local AI assistant. I can answer questions, help write code, manage reminders, open apps, search the web, "
            "and help you stay productive on your laptop. Tell me what you need."
        )
