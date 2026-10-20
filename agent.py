from tools import TOOLS
from brains.llm import decide


def run_agent(user_input):
    messages = [{"role": "user", "content": user_input}]
    max_iterations = 10

    while max_iterations > 0:
        action = decide(messages)

        if action["type"] == "final":
            return action["content"]

        elif action["type"] == "tool":
            tool_name = action["name"]
            arguments = action["arguments"]

            if tool_name not in TOOLS:
                raise ValueError(f"Tool {tool_name} not found.")

            result = TOOLS[tool_name](**arguments)

            messages.append({
                "role": "tool",
                "name": tool_name,
                "arguments": arguments,
                "result": result,
            })

        max_iterations -= 1

    raise RuntimeError("agent did not finish in max_iterations")


if __name__ == "__main__":
    print("Final result:", run_agent("What is 6 *6?"))