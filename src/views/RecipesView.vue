<script setup lang="ts">
import { onMounted, ref } from 'vue'
import Pagination from '../components/recipe/Pagination.vue'
import RecipeCard from '../components/recipe/RecipeCard.vue'
import RecipeCardSkeleton from '../components/recipe/RecipeCardSkeleton.vue'
import RecipeFilters from '../components/recipe/RecipeFilters.vue'
import { usePagination } from '../composables/usePagination'
import { useRecipeFilters } from '../composables/useRecipeFilters'
import { recipeService } from '../services/recipeService'
import type { Recipe } from '../types/recipe'

const recipes = ref<Recipe[]>([])
const isLoading = ref(true)
const errorMessage = ref<string | null>(null)

const { filters, cuisineOptions, difficultyOptions, mealTypeOptions, filteredRecipes, resetFilters } =
  useRecipeFilters(recipes)

const {
  currentPage,
  totalPages,
  paginatedItems,
  canGoPrevious,
  canGoNext,
  goToPage,
  goToPreviousPage,
  goToNextPage,
} = usePagination(filteredRecipes)

async function fetchRecipes(): Promise<void> {
  isLoading.value = true
  errorMessage.value = null

  try {
    const response = await recipeService.getRecipes()
    recipes.value = response.recipes
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Something went wrong while loading recipes.'
    recipes.value = []
  } finally {
    isLoading.value = false
  }
}

function updateFilters(nextFilters: typeof filters.value): void {
  filters.value = nextFilters
}

onMounted(() => {
  void fetchRecipes()
})
</script>

<template>
  <section class="mx-auto max-w-6xl px-5 py-12 sm:px-8 sm:py-16">
    <header class="mb-10">
      <h1 class="text-4xl font-semibold tracking-tight text-neutral-900 sm:text-5xl dark:text-white">
        Recipes
      </h1>
      <p class="mt-3 max-w-xl text-base leading-relaxed text-neutral-500 dark:text-neutral-400">
        Browse our collection of delicious recipes from around the world.
      </p>
    </header>

    <div v-if="isLoading" role="status" aria-live="polite">
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <RecipeCardSkeleton v-for="index in 12" :key="index" />
      </div>
    </div>

    <div
      v-else-if="errorMessage"
      class="rounded-2xl border border-red-200 bg-red-50 px-5 py-4"
      role="alert"
    >
      <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
      <button
        type="button"
        class="mt-3 rounded-lg bg-red-100 px-4 py-2 text-sm font-medium text-red-800 transition-colors duration-200 hover:bg-red-200"
        @click="fetchRecipes"
      >
        Try again
      </button>
    </div>

    <template v-else>
      <div class="mb-8">
        <RecipeFilters
          :filters="filters"
          :cuisine-options="cuisineOptions"
          :difficulty-options="difficultyOptions"
          :meal-type-options="mealTypeOptions"
          @update:filters="updateFilters"
          @reset="resetFilters"
        />
      </div>

      <div
        v-if="filteredRecipes.length === 0"
        class="rounded-3xl border border-dashed border-neutral-200 bg-white px-6 py-16 text-center shadow-sm dark:border-neutral-700 dark:bg-neutral-900"
      >
        <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-neutral-100 text-3xl dark:bg-neutral-800">
          🔎
        </div>
        <h2 class="mt-6 text-xl font-semibold tracking-tight text-neutral-900 dark:text-white">
          No recipes matched your filters
        </h2>
        <p class="mx-auto mt-3 max-w-md text-sm leading-relaxed text-neutral-500 dark:text-neutral-400">
          Try widening your search or clearing a few filters to explore more dishes.
        </p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <RecipeCard
            v-for="recipe in paginatedItems"
            :key="recipe.id"
            :recipe="recipe"
          />
        </div>

        <Pagination
          :current-page="currentPage"
          :total-pages="totalPages"
          :can-go-previous="canGoPrevious"
          :can-go-next="canGoNext"
          @go-to-page="goToPage"
          @previous="goToPreviousPage"
          @next="goToNextPage"
        />
      </div>
    </template>
  </section>
</template>
