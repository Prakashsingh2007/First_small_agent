def decide(messages):
    last = messages[-1]

    if last["role"] == "user":
        return {"type": "tool", "name": "add", "arguments": {"a": 1, "b": 2}}

    return {"type": "final", "content": str(last["result"])}