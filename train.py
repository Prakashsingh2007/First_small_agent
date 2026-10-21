import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

from brains.trained import prep, MODEL_PATH

TEMPLATES = {
    "add": [
        "add {a} and {b}", "{a} plus {b}", "what is {a} plus {b}", "{a} + {b}",
        "what is {a} + {b}", "sum of {a} and {b}", "total of {a} and {b}",
        "add {a} to {b}", "calculate {a} plus {b}",
    ],
    "subtract": [
        "subtract {b} from {a}", "{a} minus {b}", "what is {a} minus {b}",
        "{a} - {b}", "what is {a} - {b}", "difference of {a} and {b}",
        "deduct {b} from {a}", "calculate {a} minus {b}",
        "what is {b} subtracted from {a}",
    ],
    "multiply": [
        "multiply {a} by {b}", "multiply {a} and {b}", "{a} times {b}",
        "what is {a} times {b}", "{a} * {b}", "what is {a} * {b}",
        "calculate {a} times {b}", "{a} multiplied by {b}",
        "what is {a} multiplied by {b}",
    ],
    "divide": [
        "divide {a} by {b}", "{a} divided by {b}", "what is {a} divided by {b}",
        "{a} / {b}", "what is {a} / {b}", "calculate {a} divided by {b}",
        "quotient of {a} and {b}", "divide {a} with {b}",
    ],
}

X, y = [], []
for label, templates in TEMPLATES.items():
    for t in templates:
        X.append(prep(t.format(a=1, b=2)))
        y.append(label)

model = make_pipeline(
    TfidfVectorizer(token_pattern=r"[a-z]+|[+\-*/]", ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000),
)
model.fit(X, y)
joblib.dump(model, MODEL_PATH)
print(f"Trained on {len(X)} sentences, saved to {MODEL_PATH.name}")