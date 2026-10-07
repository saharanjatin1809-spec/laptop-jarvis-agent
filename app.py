import argparse

from jarvis.assistant import LuciferAssistant


def main():
    parser = argparse.ArgumentParser(description="Lucifer personal desktop assistant")
    parser.add_argument("--voice", action="store_true", help="start in voice mode")
    parser.add_argument("--text", action="store_true", help="start in text mode")
    args = parser.parse_args()

    assistant = LuciferAssistant()

    if args.voice:
        assistant.run_voice()
    else:
        assistant.run()


if __name__ == "__main__":
    main()
