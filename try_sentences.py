import time

from agent import run_agent

SENTENCES = [
    "add 12 and 30",
    "what is seven times eight",
    "product of 4 and 5",
    "take 8 away from 20",
    "show me 3 pictures of 5 dogs",
]

for s in SENTENCES:
    start = time.perf_counter()
    try:
        result = run_agent(s)
    except Exception as e:
        result = f"ERROR: {e}"
    print(f"{time.perf_counter() - start:5.1f}s  {s!r} -> {result}\n")