import { defineStore } from 'pinia'
import { ref } from 'vue'
import { recommendationService } from '../services/recommendationService'
import { useToastStore } from './toasts'

const STORAGE_KEY = 'ai-chef-ratings'

export const useRatingsStore = defineStore('ratings', () => {
  const toastStore = useToastStore()
  const ratings = ref<Record<number, number>>({})

  function loadRatings(): void {
    if (typeof window === 'undefined') {
      return
    }

    try {
      const savedValue = window.localStorage.getItem(STORAGE_KEY)
      ratings.value = savedValue ? (JSON.parse(savedValue) as Record<number, number>) : {}
    } catch {
      ratings.value = {}
    }
  }

  function persistRatings(): void {
    if (typeof window === 'undefined') {
      return
    }

    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ratings.value))
  }

  function getRating(recipeId: number): number {
    return ratings.value[recipeId] ?? 0
  }

  async function rateRecipe(recipeId: number, rating: number): Promise<void> {
    ratings.value = { ...ratings.value, [recipeId]: rating }
    persistRatings()
    toastStore.showToast('Thanks for rating this recipe!', 'success')

    // Sends the rating to the ML backend so it can immediately update
    // the Bernoulli Naive Bayes model (online learning).
    await recommendationService.sendRating(recipeId, rating)
  }

  loadRatings()

  return {
    ratings,
    getRating,
    rateRecipe,
  }
})