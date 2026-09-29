<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import RatingStars from '../components/recipe/RatingStars.vue'
import RecipeDetailSkeleton from '../components/recipe/RecipeDetailSkeleton.vue'
import { recommendationService } from '../services/recommendationService'
import { recipeService } from '../services/recipeService'
import { useFavoritesStore } from '../stores/favorites'
import { useRatingsStore } from '../stores/ratings'
import type { Recipe } from '../types/recipe'

const route = useRoute()
const favoritesStore = useFavoritesStore()
const ratingsStore = useRatingsStore()

const recipe = ref<Recipe | null>(null)
const isLoading = ref(true)
const errorMessage = ref<string | null>(null)

const isFavorite = computed(() =>
  recipe.value ? favoritesStore.isFavorite(recipe.value.id) : false,
)

const currentRating = computed(() =>
  recipe.value ? ratingsStore.getRating(recipe.value.id) : 0,
)

function getRecipeId(): number | null {
  const id = Number(route.params.id)
  return Number.isNaN(id) ? null : id
}

function toggleFavorite(): void {
  if (recipe.value) {
    favoritesStore.toggleFavorite(recipe.value.id)
  }
}

function handleRate(star: number): void {
  if (recipe.value) {
    void ratingsStore.rateRecipe(recipe.value.id, star)
  }
}

async function fetchRecipe(): Promise<void> {
  const id = getRecipeId()

  if (id === null) {
    recipe.value = null
    errorMessage.value = 'Invalid recipe ID.'
    isLoading.value = false
    return
  }

  isLoading.value = true
  errorMessage.value = null

  try {
    recipe.value = await recipeService.getRecipeById(id)
    // Recipe views are the weakest signal for the recommender, but they
    // still help. This is fire-and-forget so it never blocks the UI.
    void recommendationService.sendView(id)
  } catch (error) {
    recipe.value = null
    errorMessage.value =
      error instanceof Error ? error.message : 'Something went wrong while loading the recipe.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  void fetchRecipe()
})

watch(
  () => route.params.id,
  () => {
    void fetchRecipe()
  },
)
</script>

<template>
  <section class="mx-auto max-w-6xl px-5 py-12 sm:px-8 sm:py-16">
    <RouterLink
      to="/recipes"
      class="mb-8 inline-block text-sm font-medium text-neutral-500 transition-colors duration-200 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white"
    >
      &larr; Back to Recipes
    </RouterLink>

    <div v-if="isLoading">
      <RecipeDetailSkeleton />
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
        @click="fetchRecipe"
      >
        Try again
      </button>
    </div>

    <article v-else-if="recipe" class="space-y-8">
      <div class="overflow-hidden rounded-2xl bg-neutral-100 shadow-sm dark:bg-neutral-800">
        <img
          :src="recipe.image"
          :alt="recipe.name"
          class="aspect-[16/9] w-full object-cover sm:aspect-[21/9]"
        />
      </div>

      <header class="space-y-4">
        <h1 class="text-3xl font-semibold tracking-tight text-neutral-900 sm:text-4xl dark:text-white">
          {{ recipe.name }}
        </h1>

        <div class="flex flex-wrap items-center gap-3">
          <button
            type="button"
            class="rounded-full border border-neutral-200 bg-white px-3 py-2 text-sm font-medium text-neutral-700 transition hover:border-neutral-300 hover:text-neutral-900 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-200 dark:hover:border-neutral-600 dark:hover:text-white"
            @click="toggleFavorite"
          >
            {{ isFavorite ? '♥ Saved' : '♡ Save' }}
          </button>
          <span class="text-sm text-neutral-500 dark:text-neutral-400">{{ recipe.cuisine }}</span>
          <span
            class="rounded-full bg-neutral-100 px-2.5 py-1 text-xs font-medium text-neutral-700 dark:bg-neutral-800 dark:text-neutral-200"
          >
            {{ recipe.difficulty }}
          </span>
          <span class="text-sm text-neutral-500">
            {{ recipe.rating.toFixed(1) }} rating
          </span>
          <span class="text-sm text-neutral-400">&middot;</span>
          <span class="text-sm text-neutral-500 dark:text-neutral-400">
            {{ recipe.prepTimeMinutes }} min prep
          </span>
          <span class="text-sm text-neutral-400 dark:text-neutral-500">&middot;</span>
          <span class="text-sm text-neutral-500 dark:text-neutral-400">
            {{ recipe.cookTimeMinutes }} min cook
          </span>
        </div>

        <div class="flex items-center gap-3 rounded-2xl border border-neutral-200/80 bg-white px-4 py-3 dark:border-neutral-700 dark:bg-neutral-900">
          <span class="text-sm font-medium text-neutral-700 dark:text-neutral-200">
            Rate this recipe:
          </span>
          <RatingStars :model-value="currentRating" @update:model-value="handleRate" />
          <span v-if="currentRating > 0" class="text-sm text-neutral-500 dark:text-neutral-400">
            You rated this {{ currentRating }} / 5
          </span>
        </div>
      </header>

      <div class="grid gap-10 md:grid-cols-2">
        <div>
          <h2 class="mb-4 text-xl font-semibold tracking-tight text-neutral-900 dark:text-white">
            Ingredients
          </h2>
          <ul class="space-y-2">
            <li
              v-for="(ingredient, index) in recipe.ingredients"
              :key="index"
              class="flex items-start gap-2 text-sm leading-relaxed text-neutral-600 dark:text-neutral-300"
            >
              <span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-neutral-400 dark:bg-neutral-500" />
              {{ ingredient }}
            </li>
          </ul>
        </div>

        <div>
          <h2 class="mb-4 text-xl font-semibold tracking-tight text-neutral-900 dark:text-white">
            Instructions
          </h2>
          <ol class="space-y-4">
            <li
              v-for="(instruction, index) in recipe.instructions"
              :key="index"
              class="flex gap-3 text-sm leading-relaxed text-neutral-600 dark:text-neutral-300"
            >
              <span
                class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-neutral-100 text-xs font-medium text-neutral-700 dark:bg-neutral-800 dark:text-neutral-200"
              >
                {{ index + 1 }}
              </span>
              <span>{{ instruction }}</span>
            </li>
          </ol>
        </div>
      </div>
    </article>
  </section>
</template>