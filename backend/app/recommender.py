"""The core recommendation engine.

Ties together:
- the recipe dataset (recipes_data.py)
- feature extraction (feature_extraction.py)
- the online-learning model (model.py)
- persisted interaction history (storage.py)

and exposes simple functions that main.py's API endpoints call.
"""

import random
from collections import Counter

from . import feature_extraction, recipes_data, storage
from .config import (
    FAVORITE_REPEATS,
    MODERATE_RATING_REPEATS,
    STRONG_RATING_REPEATS,
    TOP_N_RECOMMENDATIONS,
    VIEW_LEARNING_INTERVAL,
)
from .model import RecipeRecommenderModel

_model = RecipeRecommenderModel()
_state = storage.load_state()


def initialize() -> None:
    """Called once when the server starts up."""
    recipes_data.load_recipes()
    _rebuild_model_from_history()


# ---------------------------------------------------------------------
# Learning from feedback
# ---------------------------------------------------------------------

def _learn_from_rating(recipe: dict, rating: int) -> None:
    """Ratings are the strongest signal (Requirement: Ratings = Highest
    Importance). 3-star ratings are neutral and are ignored entirely.
    """
    if rating == 3:
        return  # Neutral: ignored, per project specification.

    features = feature_extraction.extract_features(recipe)

    if rating == 5:
        liked, repeats = True, STRONG_RATING_REPEATS
    elif rating == 4:
        liked, repeats = True, MODERATE_RATING_REPEATS
    elif rating == 2:
        liked, repeats = False, MODERATE_RATING_REPEATS
    elif rating == 1:
        liked, repeats = False, STRONG_RATING_REPEATS
    else:
        return  # Invalid rating, ignore defensively.

    for _ in range(repeats):
        _model.learn(features, liked)


def _learn_from_favorite(recipe: dict) -> None:
    """Favorites are medium importance: always a single positive signal.

    Per the project spec, removing a favorite does NOT generate negative
    feedback — we simply stop treating the recipe as favorited.
    """
    features = feature_extraction.extract_features(recipe)
    for _ in range(FAVORITE_REPEATS):
        _model.learn(features, True)


def _learn_from_view(recipe: dict) -> None:
    """A single weak positive learning step from repeated views."""
    features = feature_extraction.extract_features(recipe)
    _model.learn(features, True)


def _rebuild_model_from_history() -> None:
    """Replays all stored history into a fresh model on startup.

    River models are not saved to disk in this simple project (that would
    add pickling complexity that isn't needed for a university demo) —
    instead we keep the raw interaction history and "replay" it as
    learn_one() calls whenever the server restarts.
    """
    recipes_by_id = recipes_data.get_recipes_by_id()

    for recipe_id_str, rating in _state["ratings"].items():
        recipe = recipes_by_id.get(int(recipe_id_str))
        if recipe:
            _learn_from_rating(recipe, rating)

    for recipe_id_str in _state["favorites"]:
        recipe = recipes_by_id.get(int(recipe_id_str))
        if recipe:
            _learn_from_favorite(recipe)

    for recipe_id_str, view_count in _state["views"].items():
        recipe = recipes_by_id.get(int(recipe_id_str))
        if recipe:
            repeats = view_count // VIEW_LEARNING_INTERVAL
            for _ in range(repeats):
                _learn_from_view(recipe)


# ---------------------------------------------------------------------
# Public functions called by the API endpoints
# ---------------------------------------------------------------------

def rate_recipe(recipe_id: int, rating: int) -> None:
    """Records a rating and immediately updates the model (online learning)."""
    recipe = recipes_data.get_recipes_by_id().get(recipe_id)

    _state["ratings"][str(recipe_id)] = rating
    storage.save_state(_state)

    if recipe:
        _learn_from_rating(recipe, rating)


def set_favorite(recipe_id: int, is_favorite: bool) -> None:
    """Adds or removes a favorite and updates the model accordingly."""
    recipe_id_str = str(recipe_id)

    if is_favorite:
        if recipe_id_str not in _state["favorites"]:
            _state["favorites"].append(recipe_id_str)
            recipe = recipes_data.get_recipes_by_id().get(recipe_id)
            if recipe:
                _learn_from_favorite(recipe)
    else:
        if recipe_id_str in _state["favorites"]:
            _state["favorites"].remove(recipe_id_str)
            # No negative learning here, per the project specification.

    storage.save_state(_state)


def record_view(recipe_id: int) -> None:
    """Tracks a recipe view and learns weakly from repeated views."""
    recipe_id_str = str(recipe_id)
    _state["views"][recipe_id_str] = _state["views"].get(recipe_id_str, 0) + 1
    storage.save_state(_state)

    view_count = _state["views"][recipe_id_str]
    if view_count % VIEW_LEARNING_INTERVAL == 0:
        recipe = recipes_data.get_recipes_by_id().get(recipe_id)
        if recipe:
            _learn_from_view(recipe)


# ---------------------------------------------------------------------
# Building recommendations + explanations
# ---------------------------------------------------------------------

def _get_liked_recipes() -> list[dict]:
    """Recipes the user rated 4+ stars, or favorited."""
    recipes_by_id = recipes_data.get_recipes_by_id()
    liked = []

    for recipe_id_str, rating in _state["ratings"].items():
        if rating >= 4:
            recipe = recipes_by_id.get(int(recipe_id_str))
            if recipe:
                liked.append(recipe)

    for recipe_id_str in _state["favorites"]:
        recipe = recipes_by_id.get(int(recipe_id_str))
        if recipe:
            liked.append(recipe)

    return liked


def _most_common_cuisine(liked_recipes: list[dict]) -> str | None:
    if not liked_recipes:
        return None
    cuisine_counts = Counter(recipe["cuisine"] for recipe in liked_recipes)
    return cuisine_counts.most_common(1)[0][0]


def _most_viewed_meal_type() -> str | None:
    recipes_by_id = recipes_data.get_recipes_by_id()
    meal_type_counts: Counter[str] = Counter()

    for recipe_id_str, view_count in _state["views"].items():
        recipe = recipes_by_id.get(int(recipe_id_str))
        if recipe:
            for meal_type in recipe.get("mealType", []):
                meal_type_counts[meal_type] += view_count

    if not meal_type_counts:
        return None
    return meal_type_counts.most_common(1)[0][0]


def _build_explanation(
    recipe: dict, favorite_cuisine: str | None, frequent_meal_type: str | None
) -> str:
    """Generates a short, human-readable reason for the recommendation."""
    if favorite_cuisine and recipe["cuisine"] == favorite_cuisine:
        return f"Recommended because you liked {favorite_cuisine} recipes."

    if frequent_meal_type and frequent_meal_type in recipe.get("mealType", []):
        return f"Recommended because you frequently view {frequent_meal_type} recipes."

    return "Recommended based on your overall taste profile so far."


def get_recommendations(top_n: int = TOP_N_RECOMMENDATIONS) -> list[dict]:
    """Returns the top N personalized recipe recommendations.

    Steps (matching the project specification):
    1. Load all recipes.
    2. Exclude recipes the user has already rated.
    3. Extract binary features for each remaining recipe.
    4. Predict "like probability" using BernoulliNB.
    5. Combine with favorite/view signals via the explanation text.
    6. Rank highest to lowest score.
    7. Return the top N.
    """
    all_recipes = recipes_data.get_all_recipes()
    rated_ids = {int(recipe_id_str) for recipe_id_str in _state["ratings"].keys()}
    candidates = [recipe for recipe in all_recipes if recipe["id"] not in rated_ids]

    has_any_interaction = bool(
        _state["ratings"] or _state["favorites"] or _state["views"]
    )

    # Cold start: brand-new user, no interactions yet -> random recipes.
    if not has_any_interaction:
        sample_size = min(top_n, len(candidates))
        sample = random.sample(candidates, sample_size)
        return [
            {
                "recipe": recipe,
                "score": 0.5,
                "explanation": "Recommended for you to discover something new.",
            }
            for recipe in sample
        ]

    liked_recipes = _get_liked_recipes()
    favorite_cuisine = _most_common_cuisine(liked_recipes)
    frequent_meal_type = _most_viewed_meal_type()

    scored_recipes = []
    for recipe in candidates:
        features = feature_extraction.extract_features(recipe)
        score = _model.predict_like_probability(features)
        explanation = _build_explanation(recipe, favorite_cuisine, frequent_meal_type)
        scored_recipes.append(
            {"recipe": recipe, "score": round(score, 3), "explanation": explanation}
        )

    scored_recipes.sort(key=lambda item: item["score"], reverse=True)
    return scored_recipes[:top_n]