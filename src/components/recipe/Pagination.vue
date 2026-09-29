<script setup lang="ts">
const props = defineProps<{
  currentPage: number
  totalPages: number
  canGoPrevious: boolean
  canGoNext: boolean
}>()

const emit = defineEmits<{
  (event: 'go-to-page', page: number): void
  (event: 'previous'): void
  (event: 'next'): void
}>()

function pageNumbers(): number[] {
  const pages: number[] = []

  for (let page = 1; page <= props.totalPages; page += 1) {
    pages.push(page)
  }

  return pages
}
</script>

<template>
  <nav v-if="totalPages > 1" class="mt-8 flex flex-wrap items-center justify-center gap-2" aria-label="Pagination">
    <button
      type="button"
      class="rounded-full border border-neutral-200 bg-white px-3 py-2 text-sm font-medium text-neutral-600 transition hover:border-neutral-300 hover:text-neutral-900 disabled:cursor-not-allowed disabled:opacity-60 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-300 dark:hover:border-neutral-600 dark:hover:text-white"
      :disabled="!canGoPrevious"
      @click="emit('previous')"
    >
      Previous
    </button>

    <button
      v-for="page in pageNumbers()"
      :key="page"
      type="button"
      class="h-10 w-10 rounded-full border text-sm font-medium transition"
      :class="page === currentPage
        ? 'border-neutral-900 bg-neutral-900 text-white dark:border-white dark:bg-white dark:text-neutral-900'
        : 'border-neutral-200 bg-white text-neutral-600 hover:border-neutral-300 hover:text-neutral-900 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-300 dark:hover:border-neutral-600 dark:hover:text-white'"
      :aria-current="page === currentPage ? 'page' : undefined"
      @click="emit('go-to-page', page)"
    >
      {{ page }}
    </button>

    <button
      type="button"
      class="rounded-full border border-neutral-200 bg-white px-3 py-2 text-sm font-medium text-neutral-600 transition hover:border-neutral-300 hover:text-neutral-900 disabled:cursor-not-allowed disabled:opacity-60 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-300 dark:hover:border-neutral-600 dark:hover:text-white"
      :disabled="!canGoNext"
      @click="emit('next')"
    >
      Next
    </button>
  </nav>
</template>
