"""Pydantic request models for the API endpoints."""

from pydantic import BaseModel


class RatingRequest(BaseModel):
    recipeId: int
    rating: int


class FavoriteRequest(BaseModel):
    recipeId: int
    isFavorite: bool


class ViewRequest(BaseModel):
    recipeId: int