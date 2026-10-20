def decide(messages):
    last = messages[-1]

    if last["role"] == "user":
        return {"type": "tool", "name": "multiply", "arguments": {"a": 4, "b": 5}}

    return {"type": "final", "content": str(last["result"])}