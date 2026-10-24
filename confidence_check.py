from brains.nlp import normalize
from brains.trained import classify

SENTENCES = [
    # wording the model knows
    "add 12 and 30", "what is 7 times 8", "subtract 15 from 40", "divide 10 by 4",
    # wording it may not know
    "product of 4 and 5", "take 8 away from 20", "what is 9 over 3",
    "how much is 50 plus 25",
    # not maths at all, but two numbers
    "show me 3 pictures of 5 dogs", "call me at 9 or 10",
]

for s in SENTENCES:
    name, conf = classify(normalize(s))
    print(f"{conf:.2f}  {name:9} {s}")