# engine/llm.py

"""
LLM Support (Optional)
----------------------
Currently a lightweight fallback text summarizer if the user chooses
to enable "AI summaries." It doesn't require a real model.

In the future, you can:
 - Connect OpenAI / Claude / Local LLM (phi-3, llama.cpp etc.)
"""

def ask_llm_usage():
    """Ask user whether they want AI-generated short highlights."""
    ans = input("🤖 Use AI summaries? (Y/N): ").strip().lower()
    return ans in ("y", "yes")


def summarize_description(text):
    """
    Simple fallback summary (no external API required).
    Just shortens long descriptions cleanly.

    Replace this with a real model call later if desired.
    """
    if not text:
        return ""

    words = text.split()
    if len(words) <= 40:
        return text.strip()

    return " ".join(words[:40]) + "..."
