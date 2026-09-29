"""Fetches and caches the recipe dataset from DummyJSON.

This mirrors what the Vue frontend already does in recipeService.ts,
so recipe IDs line up perfectly between the two.
"""

import requests

from .config import DUMMYJSON_RECIPES_URL

# Simple in-memory cache. Since this is a small university demo with
# ~50 recipes, there is no need for a database.
_all_recipes: list[dict] = []
_recipes_by_id: dict[int, dict] = {}


def load_recipes() -> None:
    """Downloads the recipe dataset once and caches it in memory."""
    global _all_recipes, _recipes_by_id

    response = requests.get(DUMMYJSON_RECIPES_URL, timeout=10)
    response.raise_for_status()
    data = response.json()

    _all_recipes = data["recipes"]
    _recipes_by_id = {recipe["id"]: recipe for recipe in _all_recipes}


def get_all_recipes() -> list[dict]:
    """Returns every recipe in the dataset."""
    if not _all_recipes:
        load_recipes()
    return _all_recipes


def get_recipes_by_id() -> dict[int, dict]:
    """Returns a dict for fast lookup of a recipe by its numeric ID."""
    if not _recipes_by_id:
        load_recipes()
    return _recipes_by_id