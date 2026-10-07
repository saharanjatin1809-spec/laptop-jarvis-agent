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

    def generate_response(self, prompt: str, mode: str = "general") -> str:
        if self.client is not None:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Lucifer, a helpful personal AI assistant for a laptop. Answer clearly, practically, and efficiently."
                        },
                        {"role": "user", "content": prompt},
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

        if any(word in lower for word in ["write", "code", "script", "python", "javascript", "html", "css", "bug", "fix", "debug", "function"]):
            return (
                "I can help with that. Start by defining the exact goal, then break the work into smaller steps and build a minimal version first. "
                "If you share the code or error, I can help fix it and explain the solution clearly."
            )

        if any(word in lower for word in ["open", "launch", "app", "website", "browser"]):
            return "I can open apps and websites for you. Tell me what you want to launch or which URL to open."

        if any(word in lower for word in ["remind", "reminder", "schedule", "alarm"]):
            return "I can set reminders. Try: 'Remind me in 20 minutes to drink water' or 'Set a reminder for 7 PM for my meeting'."

        if any(word in lower for word in ["play", "music", "song", "video"]):
            return "I can help you search for music or media. Tell me what you want played or searched."

        return (
            "I am Lucifer, your local AI assistant. I can answer questions, help write code, open apps, manage reminders, "
            "search the web, and guide you through tasks on your laptop. Tell me what you want done."
        )
