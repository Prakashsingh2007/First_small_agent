import re

UNITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}
SCALES = {"hundred", "thousand"}

_words = sorted([*UNITS, *TENS, *SCALES], key=len, reverse=True)
_W = "|".join(_words)
# a run of number words, e.g. "twenty one" or "one hundred twenty-three"
NUMBER_RUN = re.compile(rf"\b(?:{_W})(?:[\s-]+(?:{_W}))*\b")


def _run_to_int(run):
    total, current = 0, 0
    for w in re.split(r"[\s-]+", run):
        if w in UNITS:
            current += UNITS[w]
        elif w in TENS:
            current += TENS[w]
        elif w == "hundred":
            current = max(current, 1) * 100
        elif w == "thousand":
            total += max(current, 1) * 1000
            current = 0
    return total + current


def normalize(text):
    text = text.lower().replace("×", "*").replace("÷", "/")
    text = NUMBER_RUN.sub(lambda m: str(_run_to_int(m.group(0))), text)
    text = re.sub(r"\bnegative\s+(\d)", r"-\1", text)
    # "20-5" -> "20 - 5" so the minus is not read as a negative sign
    text = re.sub(r"(?<=\d)\s*([+*/-])\s*(?=\d)", r" \1 ", text)
    return text