from errors import AgentError
from tools import TOOLS
from brains.hybrid import decide


def run_agent(user_input, brain=None):
    decide_fn = brain or decide
    messages = [{"role": "user", "content": user_input}]
    max_iterations = 10

    while max_iterations > 0:
        try:
            action = decide_fn(messages)
        except ValueError as e:
            # a brain that can't parse the request (e.g. the trained brain, 3 numbers)
            raise AgentError(f"this brain could not understand the request ({e})") from e

        if action["type"] == "final":
            return action["content"]

        if action["type"] == "tool":
            tool_name = action["name"]
            arguments = action["arguments"]

            if tool_name not in TOOLS:
                raise AgentError(f"unknown tool {tool_name!r}")

            record = {"role": "tool", "name": tool_name, "arguments": arguments}
            try:
                record["result"] = TOOLS[tool_name](**arguments)
                print(f"  step: {tool_name}({arguments}) = {record['result']}")
            except (TypeError, ValueError) as e:
                record["error"] = str(e)
                print(f"  step: {tool_name}({arguments}) FAILED: {e}")
            messages.append(record)

        max_iterations -= 1

    raise AgentError("the agent did not finish within the step limit")


def answer(user_input, brain=None):
    """Never crashes: always returns text a person can read."""
    try:
        return run_agent(user_input, brain)
    except AgentError as e:
        return f"Sorry, I couldn't do that: {e}"


if __name__ == "__main__":
    print("Final result:", answer("What is 1 + 2?"))