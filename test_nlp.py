from brains.nlp import normalize
from brains.trained import decide

assert normalize("add two and three") == "add 2 and 3"
assert normalize("twenty-one plus five") == "21 plus 5"
assert normalize("one hundred twenty three minus four") == "123 minus 4"
assert normalize("two thousand five hundred") == "2500"
assert normalize("20-5") == "20 - 5"
assert normalize("negative five plus three") == "-5 plus 3"
assert normalize("3 × 4") == "3 * 4"
assert normalize("what is 10 / 4") == "what is 10 / 4"
assert normalize("someone is done") == "someone is done"   # "one" inside words is untouched

def first(text):
    return decide([{"role": "user", "content": text}])

assert first("five plus seven") == {"type": "tool", "name": "add", "arguments": {"a": 5, "b": 7}}
assert first("20-5")["arguments"] == {"a": 20, "b": 5}
assert first("subtract ten from forty")["arguments"] == {"a": 40, "b": 10}

print("All nlp tests passed")