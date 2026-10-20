from brains.parse import parse_reply, BadReply


def raises(fn, *args):
    try:
        fn(*args)
    except BadReply:
        return True
    return False


# valid replies
assert parse_reply('{"type":"tool","name":"add","arguments":{"a":1,"b":2}}') == {
    "type": "tool", "name": "add", "arguments": {"a": 1, "b": 2}
}
assert parse_reply('{"type":"final","content":3}') == {"type": "final", "content": "3"}

# the exact mistake your smoke test showed
assert raises(parse_reply, '{"type":"tool","name":"add","arguments":{"num1":1,"num2":2}}')

# other bad replies
assert raises(parse_reply, "The answer is 3")                                   # not JSON
assert raises(parse_reply, "[1, 2]")                                            # not an object
assert raises(parse_reply, '{"type":"tool","name":"power","arguments":{"a":1,"b":2}}')  # unknown tool
assert raises(parse_reply, '{"type":"tool","name":"add","arguments":{"a":1}}')  # missing argument
assert raises(parse_reply, '{"type":"tool","name":"add","arguments":{"a":1,"b":2,"c":3}}')  # extra argument
assert raises(parse_reply, '{"type":"tool","name":"add","arguments":"1,2"}')    # arguments not an object
assert raises(parse_reply, '{"type":"final"}')                                  # no content
assert raises(parse_reply, '{"type":"think"}')                                  # unknown type

print("All brain tests passed")