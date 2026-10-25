def format_number(x):
    """30.0 -> '30', 2.5 -> '2.5'"""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def finish_action(tool_msg):
    """The final answer for a single-step request, from the last tool message."""
    if "error" in tool_msg:
        return {"type": "final", "content": f"Error: {tool_msg['error']}"}
    return {"type": "final", "content": format_number(tool_msg["result"])}