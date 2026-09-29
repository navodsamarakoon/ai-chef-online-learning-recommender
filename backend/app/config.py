"""Global constants for the recommendation backend."""

# We reuse the exact same dataset the frontend already uses (DummyJSON),
# so recipe IDs match between frontend and backend. limit=100 pulls the
# whole ~50-recipe dataset instead of DummyJSON's default page size of 30.
DUMMYJSON_RECIPES_URL = "https://dummyjson.com/recipes?limit=100"

# CORS: only the local Vite dev server is allowed to call this API.
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# How many times we replay learn_one() for a given feedback event.
# River's BernoulliNB has no built-in "sample weight", so the simple,
# beginner-friendly trick we use is to call learn_one() more than once
# for stronger signals. This is what lets ratings > favorites > views
# in terms of influence on the model.
STRONG_RATING_REPEATS = 3    # 5-star or 1-star ratings
MODERATE_RATING_REPEATS = 2  # 4-star or 2-star ratings
FAVORITE_REPEATS = 1         # adding a favorite

# Recipe views are the weakest signal. Instead of learning from every
# single view, we only learn once every VIEW_LEARNING_INTERVAL views
# of the same recipe, and even then with a single learn_one() call.
VIEW_LEARNING_INTERVAL = 5

# How many recommendations to return.
TOP_N_RECOMMENDATIONS = 5