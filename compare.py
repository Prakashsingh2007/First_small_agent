import time

import brains.llm as llm
import brains.trained as trained

# held-out sentences: several use wording that is NOT in train.py
CASES = [
    ("add 12 and 30", "add", 12, 30),
    ("what is 7 times 8", "multiply", 7, 8),
    ("subtract 15 from 40", "subtract", 40, 15),
    ("divide 10 by 4", "divide", 10, 4),
    ("20 minus 5", "subtract", 20, 5),
    ("what is the sum of 2.5 and 4", "add", 2.5, 4),
    ("100 / 8", "divide", 100, 8),
    ("3 * 11", "multiply", 3, 11),
    ("how much is 50 plus 25", "add", 50, 25),
    ("product of 4 and 5", "multiply", 4, 5),
    ("take 8 away from 20", "subtract", 20, 8),
    ("what is 9 over 3", "divide", 9, 3),
]


def first_call(decide, text):
    start = time.perf_counter()
    try:
        act = decide([{"role": "user", "content": text}])
        got = (act["name"], act["arguments"]["a"], act["arguments"]["b"])
    except Exception as e:
        got = ("ERROR", str(e)[:40], None)
    return got, time.perf_counter() - start


scores = {"llm": 0, "trained": 0}
for text, name, a, b in CASES:
    expected = (name, a, b)
    print(f"\n{text!r}  expected {expected}")
    for label, brain in (("llm", llm.decide), ("trained", trained.decide)):
        got, secs = first_call(brain, text)
        ok = got == expected
        scores[label] += ok
        print(f"  {label:8} {'OK ' if ok else 'BAD'} {got}  {secs:.2f}s")

print(f"\nScore out of {len(CASES)}: {scores}")