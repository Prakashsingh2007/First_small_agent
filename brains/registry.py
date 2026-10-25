from brains import stub, trained, llm, hybrid

BRAINS = {
    "stub": stub.decide,        # demo brain: always calls add(1, 2), ignores the request
    "trained": trained.decide,  # your own model: fast, single-step only
    "llm": llm.decide,          # Ollama: any wording, multi-step, slow
    "hybrid": hybrid.decide,    # trained first, LLM when unsure or multi-step
}
DEFAULT = "hybrid"