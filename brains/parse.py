import json
from tools import TOOL_DESCRIPTIONS


class BadReply(ValueError):
    """The model's reply does not match the format the loop understands."""


# tool name -> set of required argument names, built from tools.py
PARAMS = {t["name"]: set(t["parameters"]) for t in TOOL_DESCRIPTIONS}


def parse_reply(text):
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        raise BadReply("reply is not valid JSON") from None

    if not isinstance(data, dict):
        raise BadReply("reply must be a JSON object")

    kind = data.get("type")

    if kind == "final":
        if "content" not in data:
            raise BadReply('a final reply needs a "content" key')
        return {"type": "final", "content": str(data["content"])}

    if kind == "tool":
        name = data.get("name")
        args = data.get("arguments")
        if name not in PARAMS:
            raise BadReply(f"unknown tool {name!r}, choose from {sorted(PARAMS)}")
        if not isinstance(args, dict):
            raise BadReply('"arguments" must be an object')
        if set(args) != PARAMS[name]:
            raise BadReply(
                f"{name} needs exactly these arguments {sorted(PARAMS[name])}, got {sorted(args)}"
            )
        for key, value in args.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise BadReply(
                    f"argument {key} must be a number, got {value!r}; "
                    "use the actual number from the tool result"
                )
        return {"type": "tool", "name": name, "arguments": args}
    raise BadReply('"type" must be "tool" or "final"')