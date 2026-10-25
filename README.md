# Calculator Agent

A small AI agent that turns plain-language requests such as *"add 2 and 3, then multiply the result by 4"* into calculator tool calls, runs them, and returns the answer. It has four interchangeable "brains", so you can compare a hand-trained model, a local language model, and a hybrid of the two on the same agent loop.

Built as a learning project: the goal was to understand how an agent works end to end (loop, tools, brain, validation, error handling), not just to get answers.

## Quick start

```bash
git clone https://github.com/Prakashsingh2007/First_small_agent.git
cd First_small_agent
pip install -r requirements.txt
python train.py        # trains the small intent model (run once)
python main.py
```

Then type a request at the `>` prompt, for example:

```
> add 2 to 3
> what is seven times eight
> subtract 15 from 40
> 20 - 5
> add 2 and 3, then multiply the result by 4
```

Commands inside the program:

| Command | What it does |
|---|---|
| `/brain <name>` | choose which brain answers |
| `/brains` | list the brains (`*` marks the current one) |
| `/help` | show the manual |
| `/quit` | exit |

### Optional: the language-model brains

The `llm` and `hybrid` brains use a local model through [Ollama](https://ollama.com). The `trained` and `stub` brains work without it.

```bash
ollama pull qwen2.5-coder:7b
ollama serve
```

The model needs roughly 5 GB of free RAM. The first answer can take 30+ seconds while the model loads into memory. If Ollama is not running, the agent says so in plain words instead of crashing.

## The four brains

| Brain | How it works | Strengths | Limits |
|---|---|---|---|
| `stub` | always calls `add(1, 2)` | shows the loop in its simplest form | ignores your request |
| `trained` | small scikit-learn text classifier picks the operation, a regex finds the numbers | instant, runs offline | one operation, exactly two numbers, only wording it was trained on |
| `llm` | local model via Ollama chooses the tool and arguments | any wording, multi-step requests | seconds per step, needs RAM |
| `hybrid` (default) | `trained` answers when confident, otherwise `llm`; multi-step requests go straight to `llm` | fast for common requests, flexible for the rest | threshold was tuned on a small sentence set |

All four expose the same function, `decide(messages)`, which is why they can be swapped without touching the loop.

## How it works

```
                 main.py  (choose a brain with /brain <name>)
                    │
                    ▼
              agent.py: answer() ──► run_agent() loop
                    │                    │
                    │      messages ◄────┤  user message, tool results, tool errors
                    ▼                    │
              decide(messages) ──► {"type": "tool", ...} or {"type": "final", ...}
                    │                    │
        ┌───────────┼──────────┬─────────┘
        ▼           ▼          ▼
      stub      trained       llm ──► parse.py (reply shape check) + final-answer check
                    │           ▲
                    └─ hybrid ──┘   (low confidence or multi-step → llm)

              tools.py: TOOLS[name](**arguments)   ← check_numbers rejects non-numbers
```

The loop, for `add 2 and 3, then multiply the result by 4`:

| Pass | `messages` at the start | `decide()` returns |
|---|---|---|
| 1 | `[user]` | `add(2, 3)` |
| 2 | `[user, tool(add → 5)]` | `multiply(5, 4)` |
| 3 | `[user, tool(add → 5), tool(multiply → 20)]` | `final "20"` |

The brain only chooses. It never runs anything and never does arithmetic. The loop runs the tool, appends the result to `messages`, and asks the brain again until it returns `final`.

### Safety layers

- **Tools are strict.** `check_numbers` rejects strings, `None` and booleans. Division by zero raises a clear error.
- **Brain replies are validated.** `parse.py` rejects replies that are not valid JSON, use an unknown tool, have wrong or missing argument names, or pass non-number values. The `llm` brain retries with feedback.
- **The model may not invent numbers.** A numeric final answer must come after a tool call and must equal the last tool result.
- **Failures become messages.** A failing tool is recorded as an error that the brain can explain. An unreachable model, a brain that gives up, and a runaway loop (10-step limit) all produce a readable message, never a traceback.

## Project structure

```
.
├── main.py              entry point: manual, brain selector
├── agent.py             the agent loop and the never-crashes wrapper
├── tools.py             add, subtract, multiply, divide + registry + descriptions
├── errors.py            AgentError, BrainUnavailable, BrainGaveUp
├── train.py             trains the intent classifier
├── brains/
│   ├── registry.py      name → brain lookup used by the selector
│   ├── stub.py          demo brain
│   ├── trained.py       classifier + number extraction
│   ├── llm.py           Ollama brain with retries and final-answer check
│   ├── hybrid.py        routing between trained and llm
│   ├── parse.py         validates a model's JSON reply
│   ├── nlp.py           number words, negatives, "20-5" spacing
│   └── common.py        number formatting and the finishing step
├── test_tools.py        tool behavior and input validation
├── test_nlp.py          text normalization and the trained brain
├── test_brain.py        reply validation with fake model replies
├── test_errors.py       error handling and the final-answer check
├── compare.py           runs the llm and trained brains on the same sentences
├── confidence_check.py  prints classifier confidence for sample sentences
└── try_multistep.py     end-to-end multi-step examples (needs Ollama)
```

## Tests

None of these need Ollama:

```bash
for f in test_tools.py test_nlp.py test_brain.py test_errors.py; do python $f || break; done
```

`test_nlp.py` needs the trained model, so run `python train.py` first. `try_multistep.py` and `compare.py` call the language model and need Ollama running.

## Known limits

- Tools take exactly two numbers. Longer sums work through chaining (`add 1, 2 and 3` becomes two `add` calls), and only with the `llm` or `hybrid` brain.
- Number words work up to the thousands (`twenty-one`, `two thousand five hundred`). `one hundred and five` and decimals in words (`two point five`) are not supported.
- The trained brain only knows the wording in `train.py`. Unfamiliar phrasing such as `product of 4 and 5` can be misclassified, which is why the hybrid only trusts it above a confidence threshold. That threshold (`CONFIDENCE_THRESHOLD` in `brains/hybrid.py`) was chosen from a small sentence set, so treat it as a safety net, not a guarantee.
- The final-answer check covers numeric answers. A language model's prose answers (refusals, error explanations) are accepted as written.
- No memory between requests: each request starts fresh.

## Tested on

Linux, Python 3.14, 12 GB RAM, CPU only (no GPU), Ollama with `qwen2.5-coder:7b`.

## Author

Built by Prakash ([@Prakashsingh2007](https://github.com/Prakashsingh2007)) as a step-by-step project: stub loop, strict tools, pretrained brain, self-trained brain, language handling, hybrid routing, multi-step requests, error handling.