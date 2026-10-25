"""Settings shared across the course.

Read API keys and model names from environment variables rather than hard-coding them.
"""

import os

# Default model. Set the AIE_MODEL environment variable to switch models.
#   Example: export AIE_MODEL=gemini-3.5-flash
DEFAULT_MODEL = "gemini-3.5-flash-lite" #"gemini-2.5-flash" "gemini-3.8-flash" "gemini-3.5-flash-lite"
MODEL = os.getenv("AIE_MODEL", DEFAULT_MODEL)

DEFAULT_TEMPERATURE = 0.9
TEMPERATURE = float(os.getenv("AIE_TEMPERATURE", DEFAULT_TEMPERATURE))

def api_error_message(status: int, detail: str = "") -> str:
    """Convert an HTTP status code into a student-friendly explanation (shared by ask.py and agent.py)."""
    if status == 429:
        return "Rate limit reached. Wait about 1 minute and try again."
    if status == 503:
        return "The model is busy (503). Wait a little and try again."
    if status in (400, 401, 403, 404):
        return f"There is a problem with the API key or model name ({status}): {detail}"
    return f"API error ({status}): {detail}"


def get_api_key() -> str:
    """Return the GEMINI_API_KEY environment variable. If unset, show instructions and exit."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise SystemExit(
            "The GEMINI_API_KEY environment variable was not found.\n"
            "1. Register GEMINI_API_KEY under GitHub Settings → Codespaces → Secrets,\n"
            "   and select your own fork for repository access.\n"
            "2. If you registered it after starting Codespaces, restart your Codespace.\n"
            "   (Bottom-left 'Codespaces' → 'Stop Current Codespace' → open it again)"
        )
    return key
