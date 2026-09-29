"""Turns a recipe into a binary (one-hot style) feature dictionary.

This is the "Content-Based" + "Feature Engineering" part of the project.
Each recipe becomes a dictionary like:

    {
        "cuisine=italian": True,
        "difficulty=easy": True,
        "mealtype=dinner": True,
        "ingredient=olive oil": True,
        "tag=quick": True,
        ...
    }

River's BernoulliNB is happy to work with these sparse dictionaries
directly — we don't need to build a fixed-length vector by hand.
"""


def normalize(text: str) -> str:
    """Lower-cases and trims text so 'Olive Oil' and 'olive oil ' match."""
    return text.strip().lower()


def extract_features(recipe: dict) -> dict[str, bool]:
    """Builds the binary feature dictionary for a single recipe."""
    features: dict[str, bool] = {}

    # Cuisine and difficulty are single values per recipe.
    features[f"cuisine={normalize(recipe['cuisine'])}"] = True
    features[f"difficulty={normalize(recipe['difficulty'])}"] = True

    # Meal type, ingredients and tags are lists, so each value becomes
    # its own binary feature.
    for meal_type in recipe.get("mealType", []):
        features[f"mealtype={normalize(meal_type)}"] = True

    for ingredient in recipe.get("ingredients", []):
        features[f"ingredient={normalize(ingredient)}"] = True

    for tag in recipe.get("tags", []):
        features[f"tag={normalize(tag)}"] = True

    return features


def build_vocabulary(recipes: list[dict]) -> dict[str, list[str]]:
    """Builds the full feature vocabulary automatically from the dataset.

    This is not strictly required by River (which handles sparse features
    fine without a fixed vocabulary), but it is useful to show during a
    university presentation: it proves the feature space is generated
    from the data itself, not hardcoded.
    """
    cuisines: set[str] = set()
    difficulties: set[str] = set()
    meal_types: set[str] = set()
    ingredients: set[str] = set()
    tags: set[str] = set()

    for recipe in recipes:
        cuisines.add(normalize(recipe["cuisine"]))
        difficulties.add(normalize(recipe["difficulty"]))
        for meal_type in recipe.get("mealType", []):
            meal_types.add(normalize(meal_type))
        for ingredient in recipe.get("ingredients", []):
            ingredients.add(normalize(ingredient))
        for tag in recipe.get("tags", []):
            tags.add(normalize(tag))

    return {
        "cuisines": sorted(cuisines),
        "difficulties": sorted(difficulties),
        "mealTypes": sorted(meal_types),
        "ingredients": sorted(ingredients),
        "tags": sorted(tags),
    }