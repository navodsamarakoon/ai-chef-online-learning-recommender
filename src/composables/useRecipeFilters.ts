import { computed, ref, type Ref } from 'vue'
import type { Recipe } from '../types/recipe'

export type RecipeSortOption = 'featured' | 'name-asc' | 'name-desc' | 'rating-desc' | 'cookTime-asc'

export interface RecipeFiltersState {
  search: string
  cuisine: string
  difficulty: string
  mealType: string
  sort: RecipeSortOption
}

const defaultFilters: RecipeFiltersState = {
  search: '',
  cuisine: '',
  difficulty: '',
  mealType: '',
  sort: 'featured',
}

export function useRecipeFilters(recipes: Ref<Recipe[]>) {
  const filters = ref<RecipeFiltersState>({ ...defaultFilters })

  const cuisineOptions = computed(() => {
    const cuisines = recipes.value
      .map((recipe) => recipe.cuisine)
      .filter((cuisine, index, values) => values.indexOf(cuisine) === index)
      .sort((left, right) => left.localeCompare(right))

    return cuisines
  })

  const difficultyOptions = computed(() => {
    const difficulties = recipes.value
      .map((recipe) => recipe.difficulty)
      .filter((difficulty, index, values) => values.indexOf(difficulty) === index)
      .sort((left, right) => left.localeCompare(right))

    return difficulties
  })

  const mealTypeOptions = computed(() => {
    const mealTypes = new Set<string>()

    recipes.value.forEach((recipe) => {
      recipe.mealType.forEach((mealType) => mealTypes.add(mealType))
    })

    return Array.from(mealTypes).sort((left, right) => left.localeCompare(right))
  })

  const filteredRecipes = computed(() => {
    const query = filters.value.search.trim().toLowerCase()
    const selectedCuisine = filters.value.cuisine
    const selectedDifficulty = filters.value.difficulty
    const selectedMealType = filters.value.mealType

    const matchedRecipes = recipes.value.filter((recipe) => {
      const searchableText = [recipe.name, recipe.cuisine, recipe.tags.join(' '), recipe.ingredients.join(' ')]
        .join(' ')
        .toLowerCase()

      const matchesSearch = !query || searchableText.includes(query)
      const matchesCuisine = !selectedCuisine || recipe.cuisine === selectedCuisine
      const matchesDifficulty = !selectedDifficulty || recipe.difficulty === selectedDifficulty
      const matchesMealType =
        !selectedMealType ||
        recipe.mealType.some((mealType) => mealType.toLowerCase() === selectedMealType.toLowerCase())

      return matchesSearch && matchesCuisine && matchesDifficulty && matchesMealType
    })

    return [...matchedRecipes].sort((left, right) => {
      switch (filters.value.sort) {
        case 'name-asc':
          return left.name.localeCompare(right.name)
        case 'name-desc':
          return right.name.localeCompare(left.name)
        case 'rating-desc':
          return right.rating - left.rating
        case 'cookTime-asc':
          return left.cookTimeMinutes - right.cookTimeMinutes
        case 'featured':
        default:
          return 0
      }
    })
  })

  function resetFilters(): void {
    filters.value = { ...defaultFilters }
  }

  return {
    filters,
    cuisineOptions,
    difficultyOptions,
    mealTypeOptions,
    filteredRecipes,
    resetFilters,
  }
}
