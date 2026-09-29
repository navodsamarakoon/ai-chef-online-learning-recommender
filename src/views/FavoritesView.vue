<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import RecipeCard from '../components/recipe/RecipeCard.vue'
import RecipeCardSkeleton from '../components/recipe/RecipeCardSkeleton.vue'
import { recipeService } from '../services/recipeService'
import { useFavoritesStore } from '../stores/favorites'
import type { Recipe } from '../types/recipe'

const favoritesStore = useFavoritesStore()
const recipes = ref<Recipe[]>([])
const isLoading = ref(true)
const errorMessage = ref<string | null>(null)

const favoriteRecipes = computed(() =>
  recipes.value.filter((recipe) => favoritesStore.isFavorite(recipe.id)),
)

async function fetchRecipes(): Promise<void> {
  isLoading.value = true
  errorMessage.value = null

  try {
    const response = await recipeService.getRecipes()
    recipes.value = response.recipes
  } catch (error) {
    errorMessage.value =
      error instanceof Error ? error.message : 'Something went wrong while loading favorites.'
    recipes.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  void fetchRecipes()
})
</script>

<template>
  <section class="mx-auto max-w-6xl px-5 py-16 sm:px-8 sm:py-24">
    <header class="mb-10 space-y-3">
      <h1 class="text-4xl font-semibold tracking-tight text-neutral-900 sm:text-5xl dark:text-white">
        Favorites
      </h1>
      <p class="max-w-xl text-base leading-relaxed text-neutral-500 dark:text-neutral-400">
        Keep track of the recipes you want to make again.
      </p>
    </header>

    <div v-if="isLoading" role="status" aria-live="polite">
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <RecipeCardSkeleton v-for="index in 6" :key="index" />
      </div>
    </div>

    <div
      v-else-if="errorMessage"
      class="rounded-2xl border border-red-200 bg-red-50 px-5 py-4"
      role="alert"
    >
      <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
    </div>

    <div
      v-else-if="favoriteRecipes.length === 0"
      class="rounded-3xl border border-dashed border-neutral-200 bg-white px-6 py-16 text-center shadow-sm transition-shadow duration-300 dark:border-neutral-700 dark:bg-neutral-900"
    >
      <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-neutral-100 text-3xl dark:bg-neutral-800">
        ♥
      </div>
      <h2 class="mt-6 text-xl font-semibold tracking-tight text-neutral-900 dark:text-white">
        Your favorites list is empty
      </h2>
      <p class="mx-auto mt-3 max-w-md text-sm leading-relaxed text-neutral-500 dark:text-neutral-400">
        Save recipes you love from the catalog and they’ll appear here for easy access later.
      </p>
      <RouterLink
        to="/recipes"
        class="mt-6 inline-flex items-center justify-center rounded-full bg-neutral-900 px-5 py-2.5 text-sm font-medium text-white transition-all duration-200 hover:bg-neutral-700 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 focus-visible:ring-offset-2 dark:bg-white dark:text-neutral-900 dark:hover:bg-neutral-200 dark:focus-visible:ring-offset-neutral-900"
      >
        Browse Recipes
      </RouterLink>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <RecipeCard
        v-for="recipe in favoriteRecipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </section>
</template>
