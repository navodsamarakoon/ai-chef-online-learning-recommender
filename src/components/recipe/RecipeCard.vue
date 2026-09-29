<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useFavoritesStore } from '../../stores/favorites'
import type { Recipe } from '../../types/recipe'

const props = defineProps<{
  recipe: Recipe
}>()

const favoritesStore = useFavoritesStore()
const isFavorite = computed(() => favoritesStore.isFavorite(props.recipe.id))

function toggleFavorite(event: MouseEvent): void {
  event.preventDefault()
  event.stopPropagation()
  favoritesStore.toggleFavorite(props.recipe.id)
}
</script>

<template>
  <div class="relative">
    <RouterLink :to="`/recipes/${recipe.id}`" class="block">
      <article
        class="group overflow-hidden rounded-2xl border border-neutral-200/80 bg-white shadow-sm transition-all duration-300 ease-out hover:-translate-y-1 hover:shadow-lg dark:border-neutral-700 dark:bg-neutral-900"
      >
        <div class="aspect-[4/3] overflow-hidden bg-neutral-100 dark:bg-neutral-800">
          <img
            :src="recipe.image"
            :alt="recipe.name"
            class="h-full w-full object-cover transition-transform duration-300 ease-out group-hover:scale-105"
            loading="lazy"
          />
        </div>

        <div class="space-y-3 p-5">
          <div class="space-y-1">
            <h2 class="line-clamp-2 text-lg font-semibold tracking-tight text-neutral-900 dark:text-white">
              {{ recipe.name }}
            </h2>
            <p class="text-sm text-neutral-500 dark:text-neutral-400">{{ recipe.cuisine }}</p>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <span
              class="rounded-full bg-neutral-100 px-2.5 py-1 text-xs font-medium text-neutral-700 dark:bg-neutral-800 dark:text-neutral-200"
            >
              {{ recipe.difficulty }}
            </span>
            <span class="text-sm text-neutral-500 dark:text-neutral-400">
              {{ recipe.rating.toFixed(1) }} rating
            </span>
            <span class="text-sm text-neutral-400 dark:text-neutral-500">&middot;</span>
            <span class="text-sm text-neutral-500 dark:text-neutral-400">
              {{ recipe.cookTimeMinutes }} min cook
            </span>
          </div>
        </div>
      </article>
    </RouterLink>

    <button
      type="button"
      :aria-label="isFavorite ? 'Remove from favorites' : 'Add to favorites'"
      class="absolute right-3 top-3 inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/80 bg-white/90 text-lg shadow-sm transition-all duration-200 ease-out hover:scale-105 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 focus-visible:ring-offset-2 dark:border-neutral-700 dark:bg-neutral-800/90 dark:focus-visible:ring-offset-neutral-900"
      @click="toggleFavorite"
    >
      {{ isFavorite ? '♥' : '♡' }}
    </button>
  </div>
</template>
