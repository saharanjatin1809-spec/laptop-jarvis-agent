import threading
import time

try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:  # pragma: no cover
    sr = None


class VoiceEngine:
    def __init__(self, assistant_name: str = "Lucifer"):
        self.assistant_name = assistant_name
        self.recognizer = sr.Recognizer() if sr else None
        self.microphone = sr.Microphone() if sr else None
        self.engine = pyttsx3.init() if pyttsx3 else None

    def speak(self, text: str) -> None:
        if not text:
            return
        if self.engine is not None:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
                return
            except Exception:
                pass
        print(f"{self.assistant_name}: {text}")

    def listen_once(self) -> str:
        if self.recognizer is None or self.microphone is None:
            return ""

        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            try:
                return self.recognizer.recognize_google(audio)
            except Exception:
                return ""
        except Exception:
            return ""

    def listen_for_text_mode(self) -> str:
        try:
            return input("You: ").strip()
        except KeyboardInterrupt:
            return "exit"


class VoiceThread:
    def __init__(self, callback):
        self.callback = callback
        self._thread = None
        self._stop_event = threading.Event()

    def start(self):
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        while not self._stop_event.is_set():
            time.sleep(0.2)
            if self.callback:
                self.callback()

    def stop(self):
        self._stop_event.set()
