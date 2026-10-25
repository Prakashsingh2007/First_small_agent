from brains.common import finish_action


def decide(messages):
    last = messages[-1]

    if last["role"] == "user":
        return {"type": "tool", "name": "add", "arguments": {"a": 1, "b": 2}}

    return finish_action(last)