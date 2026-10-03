from .base import tool


@tool("explain")
def explain(ctx, text: str) -> dict:
    """The LLM may only rephrase fields returned by other tools."""
    return {"text": ctx.llm.explain(text, ctx.case.language)}
