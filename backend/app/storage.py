"""Very small JSON-file based storage for user interactions.

There is no login system in this project, so we track a single user's
interaction history. This keeps the demo simple while still surviving
a backend restart (the model itself is rebuilt from this history on
startup — see recommender.py).
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "interactions.json")


def _empty_state() -> dict:
    return {
        "ratings": {},    # { "recipeId": rating (1-5) }
        "favorites": [],  # [ "recipeId", ... ]
        "views": {},      # { "recipeId": view_count }
    }


def load_state() -> dict:
    """Loads interaction history from disk, or returns an empty state."""
    if not os.path.exists(DATA_FILE):
        return _empty_state()

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state: dict) -> None:
    """Persists interaction history to disk."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)