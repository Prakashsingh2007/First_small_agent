import json
import urllib.request

from tools import TOOL_DESCRIPTIONS
from brains.parse import parse_reply, BadReply

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:7b"
MAX_RETRIES = 2

SYSTEM_TEMPLATE = """You are the decision step of a calculator agent.
You can use these tools:
__TOOLS__

Reply with ONE JSON object and nothing else, in exactly one of these formats.

To use a tool (argument names must be exactly "a" and "b"):
{"type": "tool", "name": "add", "arguments": {"a": 1, "b": 2}}

To give the final answer:
{"type": "final", "content": "3"}

Rules:
- A request may need several steps. Do ONE step at a time.
- After each tool result, either call the next tool or, if every step is finished, reply with type "final".
- "the result" means the most recent tool result. Put its actual number in the arguments.
- Argument values must be plain numbers, never words or expressions.
- Never do arithmetic yourself. Use a tool for every operation.

Example:
User: add 2 and 3, then multiply the result by 4
You: {"type": "tool", "name": "add", "arguments": {"a": 2, "b": 3}}
User: Tool result: 5
You: {"type": "tool", "name": "multiply", "arguments": {"a": 5, "b": 4}}
User: Tool result: 20
You: {"type": "final", "content": "20"}"""

SYSTEM_PROMPT = SYSTEM_TEMPLATE.replace("__TOOLS__", json.dumps(TOOL_DESCRIPTIONS, indent=2))


def to_chat(messages):
    """Convert the agent's messages into the chat format Ollama expects."""
    chat = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in messages:
        if m["role"] == "user":
            chat.append({"role": "user", "content": m["content"]})
        elif m["role"] == "tool":
            call = {"type": "tool", "name": m["name"], "arguments": m.get("arguments", {})}
            chat.append({"role": "assistant", "content": json.dumps(call)})
            chat.append({"role": "user", "content": f'Tool result: {m["result"]}'})
    return chat


def ask_model(chat):
    body = json.dumps({
        "model": MODEL,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0},
        "messages": chat,
    }).encode()
    req = urllib.request.Request(
        OLLAMA_URL, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read())["message"]["content"]


def decide(messages):
    chat = to_chat(messages)
    last_error = None

    for _ in range(MAX_RETRIES + 1):
        reply = ask_model(chat)
        try:
            return parse_reply(reply)
        except BadReply as e:
            last_error = e
            chat.append({"role": "assistant", "content": reply})
            chat.append({
                "role": "user",
                "content": f"Invalid reply: {e}. Reply again with valid JSON in the required format.",
            })

    raise RuntimeError(f"model gave an invalid reply after retries: {last_error}")