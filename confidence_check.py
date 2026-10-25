from brains.nlp import normalize
from brains.trained import classify

SENTENCES = [
    "add 12 and 30", "what is 7 times 8", "subtract 15 from 40", "divide 10 by 4",
    "product of 4 and 5", "take 8 away from 20", "what is 9 over 3", "how much is 50 plus 25",
    "my flight leaves at 6 from gate 12", "chapter 3 has 40 pages",
    "send 5 emails to 20 people", "it is 9 degrees and 14 outside",
]

for s in SENTENCES:
    name, conf = classify(normalize(s))
    print(f"{conf:.2f}  {name:9} {s}")