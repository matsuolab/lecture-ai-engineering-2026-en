"""Settings shared across the course.

Read API keys and model names from environment variables rather than hard-coding them.
"""

import os
from dotenv import find_dotenv, load_dotenv

# Load local environment files if present (.env.local takes precedence over .env)
load_dotenv(find_dotenv(".env.local"))
load_dotenv(find_dotenv(".env"))

# Default model. Set the AIE_MODEL environment variable to switch models.
#   Example: export AIE_MODEL=gemini-3.5-flash
DEFAULT_MODEL = "gemini-3.5-flash-lite"
MODEL = os.getenv("AIE_MODEL", DEFAULT_MODEL)


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
            "- For local development: create a .env or .env.local file (see .env.example),\n"
            "  or export it in your terminal: export GEMINI_API_KEY=\"your_api_key\"\n"
            "- For GitHub Codespaces: register GEMINI_API_KEY under GitHub Settings → Codespaces → Secrets,\n"
            "  and select your fork for repository access. Restart your Codespace if newly added."
        )
    return key
