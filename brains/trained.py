import re
from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).with_name("intent_model.joblib")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
_model = None


def prep(text):
    """Replace every number with 'num' so the model learns words, not digits."""
    return NUMBER.sub(" num ", text.lower())


def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def extract_numbers(text):
    return [float(t) if "." in t else int(t) for t in NUMBER.findall(text)]


def decide(messages):
    last = messages[-1]

    # a tool result is the last message, so the task is finished
    if last["role"] != "user":
        return {"type": "final", "content": str(last["result"])}

    text = last["content"]
    nums = extract_numbers(text)
    if len(nums) != 2:
        raise ValueError(f"expected exactly 2 numbers, found {nums}")

    name = str(get_model().predict([prep(text)])[0])
    a, b = nums
    # "subtract 15 from 40" means 40 - 15, so the order flips
    if name == "subtract" and "from" in text.lower():
        a, b = b, a

    return {"type": "tool", "name": name, "arguments": {"a": a, "b": b}}