import { defineStore } from 'pinia'
import { ref } from 'vue'
import { recommendationService } from '../services/recommendationService'
import { useToastStore } from './toasts'

const STORAGE_KEY = 'ai-chef-favorites'

export const useFavoritesStore = defineStore('favorites', () => {
  const toastStore = useToastStore()
  const favoriteIds = ref<number[]>([])

  function loadFavorites(): void {
    if (typeof window === 'undefined') {
      return
    }

    try {
      const savedValue = window.localStorage.getItem(STORAGE_KEY)

      if (!savedValue) {
        favoriteIds.value = []
        return
      }

      const parsedValue = JSON.parse(savedValue) as unknown

      if (Array.isArray(parsedValue)) {
        favoriteIds.value = parsedValue.filter(
          (value): value is number => typeof value === 'number' && Number.isFinite(value),
        )
      } else {
        favoriteIds.value = []
      }
    } catch {
      favoriteIds.value = []
    }
  }

  function persistFavorites(): void {
    if (typeof window === 'undefined') {
      return
    }

    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(favoriteIds.value))
  }

  function addFavorite(id: number): void {
    if (!favoriteIds.value.includes(id)) {
      favoriteIds.value = [...favoriteIds.value, id]
      toastStore.showToast('Recipe added to favorites', 'success')
      // Favorites are a medium-importance signal for the recommender.
      void recommendationService.sendFavorite(id, true)
    }

    persistFavorites()
  }

  function removeFavorite(id: number): void {
    if (favoriteIds.value.includes(id)) {
      favoriteIds.value = favoriteIds.value.filter((favoriteId) => favoriteId !== id)
      toastStore.showToast('Recipe removed from favorites', 'info')
      // Removing a favorite just clears the status; no negative learning.
      void recommendationService.sendFavorite(id, false)
    }

    persistFavorites()
  }

  function toggleFavorite(id: number): void {
    if (isFavorite(id)) {
      removeFavorite(id)
      return
    }

    addFavorite(id)
  }

  function isFavorite(id: number): boolean {
    return favoriteIds.value.includes(id)
  }

  loadFavorites()

  return {
    favoriteIds,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    isFavorite,
  }
})