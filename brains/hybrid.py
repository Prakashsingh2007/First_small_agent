import re

from brains import trained, llm
from brains.nlp import normalize

CONFIDENCE_THRESHOLD = 0.5   # you deferred the re-measuring, so keep your current value
SEQUENCE = re.compile(r"\b(then|after that|afterwards|next|finally|the result|the answer)\b")


def is_multistep(text):
    t = normalize(text)
    return bool(SEQUENCE.search(t)) or len(trained.extract_numbers(t)) > 2


def decide(messages):
    last = messages[-1]
    request = messages[0]["content"]

    # multi-step: the LLM decides every step, including when to stop
    if is_multistep(request):
        if len(messages) == 1:
            print("[multi-step: LLM]")
        return llm.decide(messages)

    # single step: finishing needs no model
    if last["role"] != "user":
        return {"type": "final", "content": str(last["result"])}

    try:
        action, confidence = trained.interpret(last["content"])
        if confidence >= CONFIDENCE_THRESHOLD:
            print(f"[trained brain, confidence {confidence:.2f}]")
            return action
    except ValueError:
        pass

    print("[falling back to LLM]")
    return llm.decide(messages)