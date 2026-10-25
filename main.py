from agent import answer
from brains.llm import MODEL
from brains.registry import BRAINS, DEFAULT

MANUAL = f"""
==================== CALCULATOR AGENT ====================
Type a calculation in plain words. The agent picks a tool
(add, subtract, multiply, divide) and works it out.

Examples
  add 2 to 3
  what is seven times eight
  subtract 15 from 40
  20 - 5
  add 2 and 3, then multiply the result by 4

Commands
  /brain <name>   choose which brain answers
  /brains         list the brains (* marks the current one)
  /help           show this manual again
  /quit           exit

Brains
  hybrid    (default) fast trained brain first; language model when
            unsure or for multi-step requests
  trained   our own small model: instant, one operation, two numbers,
            limited wording
  llm       language model via Ollama: any wording, multi-step, slower
  stub      demo brain: always adds 1 and 2 (shows how the loop works)

Notes
  llm and hybrid need Ollama running (`ollama serve`) with the
  {MODEL} model. The first llm answer can take 30+ seconds while
  the model loads.
==========================================================
"""


def main():
    name = DEFAULT
    print(MANUAL)
    print(f"Current brain: {name}")

    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not text:
            continue
        if text == "/quit":
            break
        if text == "/help":
            print(MANUAL)
            continue
        if text == "/brains":
            for n in BRAINS:
                print(("* " if n == name else "  ") + n)
            continue
        if text.startswith("/brain"):
            parts = text.split()
            if len(parts) == 2 and parts[1] in BRAINS:
                name = parts[1]
                print(f"Brain set to {name}")
            else:
                print(f"Choose one of: {', '.join(BRAINS)}")
            continue

        print(answer(text, brain=BRAINS[name]))


if __name__ == "__main__":
    main()