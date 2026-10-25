import re
from pathlib import Path

import joblib

from brains.nlp import normalize
from brains.common import finish_action
from errors import BrainUnavailable

MODEL_PATH = Path(__file__).with_name("intent_model.joblib")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
_model = None


def prep(text):
    """Replace every number with 'num' so the model learns words, not digits."""
    return NUMBER.sub(" num ", text.lower())


def get_model():
    global _model
    if _model is None:
        try:
            _model = joblib.load(MODEL_PATH)
        except FileNotFoundError:
            raise BrainUnavailable(
                "the trained model file is missing. Run `python train.py` first."
            ) from None
    return _model


def extract_numbers(text):
    return [float(t) if "." in t else int(t) for t in NUMBER.findall(text)]


def classify(text):
    """Return (intent, confidence) for already-normalized text."""
    model = get_model()
    probs = model.predict_proba([prep(text)])[0]
    best = probs.argmax()
    return str(model.classes_[best]), float(probs[best])


def interpret(raw_text):
    """Turn a sentence into (tool_call, confidence). Raises ValueError if it can't."""
    text = normalize(raw_text)
    nums = extract_numbers(text)
    if len(nums) != 2:
        raise ValueError(f"expected exactly 2 numbers, found {nums}")

    name, confidence = classify(text)
    if name == "none":
        raise ValueError("not a calculation")
    a, b = nums
    # "subtract 15 from 40" means 40 - 15, so the order flips
    if name == "subtract" and "from" in text:
        a, b = b, a

    return {"type": "tool", "name": name, "arguments": {"a": a, "b": b}}, confidence


def decide(messages):
    last = messages[-1]

    # a tool result is the last message, so the task is finished
    if last["role"] != "user":
        return finish_action(last)

    action, _ = interpret(last["content"])
    return action