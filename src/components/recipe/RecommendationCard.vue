<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type { RecommendedRecipe } from '../../types/recommendation'

defineProps<{
  recommendation: RecommendedRecipe
}>()
</script>

<template>
  <RouterLink :to="`/recipes/${recommendation.recipe.id}`" class="block">
    <article
      class="group overflow-hidden rounded-2xl border border-neutral-200/80 bg-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-lg dark:border-neutral-700 dark:bg-neutral-900"
    >
      <div class="aspect-[4/3] overflow-hidden bg-neutral-100 dark:bg-neutral-800">
        <img
          :src="recommendation.recipe.image"
          :alt="recommendation.recipe.name"
          class="h-full w-full object-cover transition-transform duration-300 ease-out group-hover:scale-105"
          loading="lazy"
        />
      </div>

      <div class="space-y-3 p-5">
        <div class="space-y-1">
          <h2
            class="line-clamp-2 text-lg font-semibold tracking-tight text-neutral-900 dark:text-white"
          >
            {{ recommendation.recipe.name }}
          </h2>
          <p class="text-sm text-neutral-500 dark:text-neutral-400">
            {{ recommendation.recipe.cuisine }}
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <span
            class="rounded-full bg-neutral-100 px-2.5 py-1 text-xs font-medium text-neutral-700 dark:bg-neutral-800 dark:text-neutral-200"
          >
            {{ recommendation.recipe.difficulty }}
          </span>
          <span
            class="rounded-full bg-emerald-100 px-2.5 py-1 text-xs font-medium text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-200"
          >
            {{ Math.round(recommendation.score * 100) }}% match
          </span>
        </div>

        <p class="text-sm leading-relaxed text-neutral-500 dark:text-neutral-400">
          {{ recommendation.explanation }}
        </p>
      </div>
    </article>
  </RouterLink>
</template>