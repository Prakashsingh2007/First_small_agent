import time

from agent import run_agent

CASES = [
    ("add 2 and 3, then multiply the result by 4", 20),
    ("multiply 6 by 7, then subtract 2 from the result", 40),
    ("add 1, 2 and 3", 6),
    ("divide 100 by 4, then add 5", 30),
    ("subtract 3 from 10, then multiply by 2, then add 1", 15),
    ("add 5 and 5", 10),   # single step: must NOT use the multi-step path
]

for text, expected in CASES:
    start = time.perf_counter()
    try:
        result = run_agent(text)
        ok = float(result) == expected
    except Exception as e:
        result, ok = f"ERROR: {e}", False
    print(f"{'OK ' if ok else 'BAD'} {time.perf_counter() - start:5.1f}s  {text!r} -> {result} (expected {expected})\n")