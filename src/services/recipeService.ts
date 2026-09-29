import { DUMMYJSON_BASE_URL } from '../config/api'
import type { Recipe, RecipesResponse } from '../types/recipe'

export class RecipeService {
  async getRecipes(): Promise<RecipesResponse> {
    try {
      const response = await fetch(`${DUMMYJSON_BASE_URL}/recipes?limit=100`)

      if (!response.ok) {
        throw new Error(`Failed to fetch recipes: ${response.status} ${response.statusText}`)
      }

      const data: RecipesResponse = await response.json()
      return data
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error('An unexpected error occurred while fetching recipes')
    }
  }

  async getRecipeById(id: number): Promise<Recipe> {
    try {
      const response = await fetch(`${DUMMYJSON_BASE_URL}/recipes/${id}`)

      if (!response.ok) {
        throw new Error(`Failed to fetch recipe ${id}: ${response.status} ${response.statusText}`)
      }

      const data: Recipe = await response.json()
      return data
    } catch (error) {
      if (error instanceof Error) {
        throw error
      }
      throw new Error(`An unexpected error occurred while fetching recipe ${id}`)
    }
  }
}

export const recipeService = new RecipeService()
