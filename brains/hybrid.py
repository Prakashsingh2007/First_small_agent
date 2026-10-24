from brains import trained, llm

CONFIDENCE_THRESHOLD = 0.5   # replace with the value you measured


def decide(messages):
    last = messages[-1]

    # finishing needs no model: just report the tool result
    if last["role"] != "user":
        return {"type": "final", "content": str(last["result"])}

    try:
        action, confidence = trained.interpret(last["content"])
        if confidence >= CONFIDENCE_THRESHOLD:
            print(f"[trained brain, confidence {confidence:.2f}]")
            return action
    except ValueError:
        pass   # wrong number of numbers: let the LLM try

    print("[falling back to LLM]")
    return llm.decide(messages)