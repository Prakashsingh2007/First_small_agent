import agent
from brains.common import finish_action, format_number
from brains.llm import check_final
from brains.parse import BadReply


def raises(fn, *args):
    try:
        fn(*args)
    except BadReply:
        return True
    return False


# number formatting
assert format_number(30.0) == "30"
assert format_number(2.5) == "2.5"
assert format_number(7) == "7"

# a failing tool does not crash the loop
def fake_decide(messages):
    if messages[-1]["role"] == "user":
        return {"type": "tool", "name": "divide", "arguments": {"a": 10, "b": 0}}
    return finish_action(messages[-1])

agent.decide = fake_decide
assert agent.answer("divide 10 by 0") == "Error: Division by zero"

# a runaway brain stops at the step limit
agent.decide = lambda m: {"type": "tool", "name": "add", "arguments": {"a": 1, "b": 1}}
assert agent.answer("loop forever").startswith("Sorry")

# check_final: a brain may not invent numbers
user = [{"role": "user", "content": "add 2 and 3"}]
tool = user + [{"role": "tool", "name": "add", "arguments": {"a": 2, "b": 3}, "result": 5}]
assert raises(check_final, {"type": "final", "content": "5"}, user)      # no tool used
assert raises(check_final, {"type": "final", "content": "6"}, tool)      # wrong number
check_final({"type": "final", "content": "5"}, tool)                     # ok
check_final({"type": "final", "content": "5.0"}, tool)                   # ok
check_final({"type": "final", "content": "I can't do that"}, user)       # prose is fine

print("All error-handling tests passed")