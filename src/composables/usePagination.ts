import { computed, ref, watch, type Ref } from 'vue'

const RECIPES_PER_PAGE = 12

export function usePagination<T>(items: Ref<T[]>) {
  const currentPage = ref(1)
  const itemsPerPage = RECIPES_PER_PAGE

  const totalPages = computed(() => {
    if (items.value.length === 0) {
      return 1
    }

    return Math.max(1, Math.ceil(items.value.length / itemsPerPage))
  })

  const paginatedItems = computed(() => {
    const startIndex = (currentPage.value - 1) * itemsPerPage
    const endIndex = startIndex + itemsPerPage

    return items.value.slice(startIndex, endIndex)
  })

  const canGoPrevious = computed(() => currentPage.value > 1)
  const canGoNext = computed(() => currentPage.value < totalPages.value)

  function goToPage(page: number): void {
    const safePage = Math.min(Math.max(1, page), totalPages.value)
    currentPage.value = safePage
  }

  function goToPreviousPage(): void {
    if (canGoPrevious.value) {
      currentPage.value -= 1
    }
  }

  function goToNextPage(): void {
    if (canGoNext.value) {
      currentPage.value += 1
    }
  }

  watch(items, () => {
    currentPage.value = 1
  })

  return {
    currentPage,
    totalPages,
    paginatedItems,
    itemsPerPage,
    canGoPrevious,
    canGoNext,
    goToPage,
    goToPreviousPage,
    goToNextPage,
  }
}
