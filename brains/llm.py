import json
import urllib.error
import urllib.request

from errors import BrainUnavailable, BrainGaveUp
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
- The final answer for a calculation must be the number from the last tool result.
- If a tool returns an error, reply with type "final" and explain the problem in plain words. Do not retry a call that failed.

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
            if "error" in m:
                feedback = f'Tool error: {m["error"]}'
            else:
                feedback = f'Tool result: {m["result"]}'
            chat.append({"role": "user", "content": feedback})
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
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())["message"]["content"]
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        raise BrainUnavailable(
            "the language model is not reachable. Start it with `ollama serve` and try again."
        ) from e


def check_final(action, messages):
    """Reject a numeric final answer that the tools did not produce."""
    if action["type"] != "final":
        return
    try:
        claimed = float(action["content"])
    except ValueError:
        return   # prose (a refusal, an error explanation) is allowed

    tool_msgs = [m for m in messages if m["role"] == "tool"]
    if not tool_msgs:
        raise BadReply("do not calculate yourself; call a tool first")
    last = tool_msgs[-1]
    if "result" in last and claimed != float(last["result"]):
        raise BadReply(
            f"the final answer must equal the last tool result, which was {last['result']}"
        )


def decide(messages):
    chat = to_chat(messages)
    last_error = None

    for _ in range(MAX_RETRIES + 1):
        reply = ask_model(chat)
        try:
            action = parse_reply(reply)
            check_final(action, messages)
            return action
        except BadReply as e:
            last_error = e
            chat.append({"role": "assistant", "content": reply})
            chat.append({
                "role": "user",
                "content": f"Invalid reply: {e}. Reply again with valid JSON in the required format.",
            })

    raise BrainGaveUp(f"the model gave an invalid reply after retries: {last_error}")