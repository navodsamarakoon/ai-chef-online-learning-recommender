import { RECOMMENDATION_API_BASE_URL } from '../config/api'
import type { RecommendedRecipe } from '../types/recommendation'

// Talks to the Python ML backend that runs the River BernoulliNB
// online-learning recommendation model.
export class RecommendationService {
  async sendRating(recipeId: number, rating: number): Promise<void> {
    await this.postJson('/interactions/rating', { recipeId, rating })
  }

  async sendFavorite(recipeId: number, isFavorite: boolean): Promise<void> {
    await this.postJson('/interactions/favorite', { recipeId, isFavorite })
  }

  async sendView(recipeId: number): Promise<void> {
    await this.postJson('/interactions/view', { recipeId })
  }

  async getRecommendations(): Promise<RecommendedRecipe[]> {
    const response = await fetch(`${RECOMMENDATION_API_BASE_URL}/recommendations`)

    if (!response.ok) {
      throw new Error(
        `Failed to fetch recommendations: ${response.status} ${response.statusText}`,
      )
    }

    return (await response.json()) as RecommendedRecipe[]
  }

  private async postJson(path: string, body: unknown): Promise<void> {
    try {
      await fetch(`${RECOMMENDATION_API_BASE_URL}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
    } catch (error) {
      // Interaction tracking should never break the user experience,
      // so failures here are only logged, not thrown further.
      console.warn('Failed to send interaction to recommendation service', error)
    }
  }
}

export const recommendationService = new RecommendationService()