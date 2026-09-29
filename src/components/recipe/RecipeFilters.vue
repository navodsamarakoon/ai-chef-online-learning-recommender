<script setup lang="ts">
import { computed } from 'vue'
import type { RecipeFiltersState, RecipeSortOption } from '../../composables/useRecipeFilters'

const props = defineProps<{
  filters: RecipeFiltersState
  cuisineOptions: string[]
  difficultyOptions: string[]
  mealTypeOptions: string[]
}>()

const emit = defineEmits<{
  (event: 'update:filters', value: RecipeFiltersState): void
  (event: 'reset'): void
}>()

const sortOptions: Array<{ value: RecipeSortOption; label: string }> = [
  { value: 'featured', label: 'Featured' },
  { value: 'name-asc', label: 'Name (A–Z)' },
  { value: 'name-desc', label: 'Name (Z–A)' },
  { value: 'rating-desc', label: 'Highest rated' },
  { value: 'cookTime-asc', label: 'Fastest cook time' },
]

const hasActiveFilters = computed(() => {
  const { search, cuisine, difficulty, mealType, sort } = props.filters

  return Boolean(search || cuisine || difficulty || mealType || sort !== 'featured')
})

function updateFilter<K extends keyof RecipeFiltersState>(key: K, value: RecipeFiltersState[K]): void {
  emit('update:filters', {
    ...props.filters,
    [key]: value,
  })
}
</script>

<template>
  <section class="rounded-2xl border border-neutral-200/80 bg-white p-5 shadow-sm sm:p-6 dark:border-neutral-700 dark:bg-neutral-900">
    <div class="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between xl:gap-5">
      <div class="min-w-0 flex-1 xl:max-w-[320px]">
        <label for="recipe-search" class="mb-2 block h-5 text-sm font-medium leading-5 text-neutral-700 dark:text-neutral-200">
          Search
        </label>
        <input
          id="recipe-search"
          :value="filters.search"
          type="search"
          placeholder="Search recipes"
          class="h-11 w-full rounded-xl border border-neutral-200 bg-neutral-50 px-4 text-sm text-neutral-900 shadow-sm transition-all duration-200 placeholder:text-neutral-400 focus:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-200 focus:ring-offset-0 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:placeholder:text-neutral-500 dark:focus:border-neutral-500 dark:focus:ring-neutral-700"
          @input="updateFilter('search', ($event.target as HTMLInputElement).value)"
        />
      </div>

      <div class="flex flex-wrap gap-4 sm:gap-5 xl:flex-nowrap xl:gap-4">
        <div class="min-w-[150px] flex-1 xl:flex-none">
          <label for="recipe-cuisine" class="mb-2 block h-5 text-sm font-medium leading-5 text-neutral-700 dark:text-neutral-200">
            Cuisine
          </label>
          <select
            id="recipe-cuisine"
            :value="filters.cuisine"
            class="h-11 w-full min-w-[150px] rounded-xl border border-neutral-200 bg-neutral-50 px-4 text-sm text-neutral-900 shadow-sm transition-all duration-200 focus:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-200 focus:ring-offset-0 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:focus:border-neutral-500 dark:focus:ring-neutral-700"
            @change="updateFilter('cuisine', ($event.target as HTMLSelectElement).value)"
          >
            <option value="">All cuisines</option>
            <option v-for="cuisine in cuisineOptions" :key="cuisine" :value="cuisine">
              {{ cuisine }}
            </option>
          </select>
        </div>

        <div class="min-w-[170px] flex-1 xl:flex-none">
          <label for="recipe-difficulty" class="mb-2 block h-5 text-sm font-medium leading-5 text-neutral-700 dark:text-neutral-200">
            Difficulty
          </label>
          <select
            id="recipe-difficulty"
            :value="filters.difficulty"
            class="h-11 w-full min-w-[170px] rounded-xl border border-neutral-200 bg-neutral-50 px-4 text-sm text-neutral-900 shadow-sm transition-all duration-200 focus:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-200 focus:ring-offset-0 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:focus:border-neutral-500 dark:focus:ring-neutral-700"
            @change="updateFilter('difficulty', ($event.target as HTMLSelectElement).value)"
          >
            <option value="">All difficulties</option>
            <option v-for="difficulty in difficultyOptions" :key="difficulty" :value="difficulty">
              {{ difficulty }}
            </option>
          </select>
        </div>

        <div class="min-w-[170px] flex-1 xl:flex-none">
          <label for="recipe-meal-type" class="mb-2 block h-5 text-sm font-medium leading-5 text-neutral-700 dark:text-neutral-200">
            Meal type
          </label>
          <select
            id="recipe-meal-type"
            :value="filters.mealType"
            class="h-11 w-full min-w-[170px] rounded-xl border border-neutral-200 bg-neutral-50 px-4 text-sm text-neutral-900 shadow-sm transition-all duration-200 focus:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-200 focus:ring-offset-0 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:focus:border-neutral-500 dark:focus:ring-neutral-700"
            @change="updateFilter('mealType', ($event.target as HTMLSelectElement).value)"
          >
            <option value="">All meal types</option>
            <option v-for="mealType in mealTypeOptions" :key="mealType" :value="mealType">
              {{ mealType }}
            </option>
          </select>
        </div>

        <div class="min-w-[140px] flex-1 xl:flex-none">
          <label for="recipe-sort" class="mb-2 block h-5 text-sm font-medium leading-5 text-neutral-700 dark:text-neutral-200">
            Sort
          </label>
          <select
            id="recipe-sort"
            :value="filters.sort"
            class="h-11 w-full min-w-[140px] rounded-xl border border-neutral-200 bg-neutral-50 px-4 text-sm text-neutral-900 shadow-sm transition-all duration-200 focus:border-neutral-400 focus:outline-none focus:ring-2 focus:ring-neutral-200 focus:ring-offset-0 dark:border-neutral-700 dark:bg-neutral-800 dark:text-white dark:focus:border-neutral-500 dark:focus:ring-neutral-700"
            @change="updateFilter('sort', ($event.target as HTMLSelectElement).value as RecipeSortOption)"
          >
            <option v-for="option in sortOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div v-if="hasActiveFilters" class="mt-4 flex justify-end">
      <button
        type="button"
        class="rounded-full px-3 py-2 text-sm font-medium text-neutral-500 transition-all duration-200 hover:bg-neutral-100 hover:text-neutral-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 focus-visible:ring-offset-2 dark:text-neutral-400 dark:hover:bg-neutral-800 dark:hover:text-white dark:focus-visible:ring-offset-neutral-900"
        @click="emit('reset')"
      >
        Clear filters
      </button>
    </div>
  </section>
</template>
