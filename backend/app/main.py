"""FastAPI entry point for the recommendation backend.

Run with:
    uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import recommender
from .config import ALLOWED_ORIGINS
from .schemas import FavoriteRequest, RatingRequest, ViewRequest

app = FastAPI(title="AI Chef Recommendation Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    recommender.initialize()


@app.post("/api/interactions/rating")
def post_rating(payload: RatingRequest) -> dict:
    if not 1 <= payload.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    recommender.rate_recipe(payload.recipeId, payload.rating)
    return {"status": "ok"}


@app.post("/api/interactions/favorite")
def post_favorite(payload: FavoriteRequest) -> dict:
    recommender.set_favorite(payload.recipeId, payload.isFavorite)
    return {"status": "ok"}


@app.post("/api/interactions/view")
def post_view(payload: ViewRequest) -> dict:
    recommender.record_view(payload.recipeId)
    return {"status": "ok"}


@app.get("/api/recommendations")
def get_recommendations() -> list[dict]:
    return recommender.get_recommendations()