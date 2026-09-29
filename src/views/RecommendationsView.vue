<script setup lang="ts">
import { onMounted, ref } from 'vue'
import RecipeCardSkeleton from '../components/recipe/RecipeCardSkeleton.vue'
import RecommendationCard from '../components/recipe/RecommendationCard.vue'
import { recommendationService } from '../services/recommendationService'
import type { RecommendedRecipe } from '../types/recommendation'

const recommendations = ref<RecommendedRecipe[]>([])
const isLoading = ref(true)
const errorMessage = ref<string | null>(null)

async function fetchRecommendations(): Promise<void> {
  isLoading.value = true
  errorMessage.value = null

  try {
    recommendations.value = await recommendationService.getRecommendations()
  } catch (error) {
    errorMessage.value =
      error instanceof Error
        ? error.message
        : 'Something went wrong while loading your recommendations.'
    recommendations.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  void fetchRecommendations()
})
</script>

<template>
  <section class="mx-auto max-w-6xl px-5 py-12 sm:px-8 sm:py-16">
    <header class="mb-10 space-y-3">
      <h1 class="text-4xl font-semibold tracking-tight text-neutral-900 sm:text-5xl dark:text-white">
        Recommended For You
      </h1>
      <p class="max-w-xl text-base leading-relaxed text-neutral-500 dark:text-neutral-400">
        Personalized picks powered by an online-learning Bernoulli Naive Bayes model
        that updates every time you rate, favorite, or view a recipe.
      </p>
    </header>

    <div v-if="isLoading" role="status" aria-live="polite">
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <RecipeCardSkeleton v-for="index in 5" :key="index" />
      </div>
    </div>

    <div
      v-else-if="errorMessage"
      class="rounded-2xl border border-red-200 bg-red-50 px-5 py-4"
      role="alert"
    >
      <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
      <p class="mt-2 text-sm text-red-700">
        Make sure the recommendation backend is running at
        <code>http://localhost:8000</code>.
      </p>
      <button
        type="button"
        class="mt-3 rounded-lg bg-red-100 px-4 py-2 text-sm font-medium text-red-800 transition-colors duration-200 hover:bg-red-200"
        @click="fetchRecommendations"
      >
        Try again
      </button>
    </div>

    <div
      v-else-if="recommendations.length === 0"
      class="rounded-3xl border border-dashed border-neutral-200 bg-white px-6 py-16 text-center shadow-sm dark:border-neutral-700 dark:bg-neutral-900"
    >
      <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-neutral-100 text-3xl dark:bg-neutral-800">
        🍳
      </div>
      <h2 class="mt-6 text-xl font-semibold tracking-tight text-neutral-900 dark:text-white">
        No recommendations yet
      </h2>
      <p class="mx-auto mt-3 max-w-md text-sm leading-relaxed text-neutral-500 dark:text-neutral-400">
        Rate, favorite, or view a few recipes and check back here.
      </p>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <RecommendationCard
        v-for="recommendation in recommendations"
        :key="recommendation.recipe.id"
        :recommendation="recommendation"
      />
    </div>
  </section>
</template>