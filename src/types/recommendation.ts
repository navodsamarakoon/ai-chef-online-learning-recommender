import type { Recipe } from './recipe'

export interface RecommendedRecipe {
  recipe: Recipe
  score: number
  explanation: string
}