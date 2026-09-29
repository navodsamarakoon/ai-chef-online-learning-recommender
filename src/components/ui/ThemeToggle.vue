<script setup lang="ts">
import { useTheme } from '../../composables/useTheme'

const { isDark, toggleTheme } = useTheme()
</script>

<template>
  <button
    type="button"
    class="inline-flex items-center justify-center rounded-full border border-neutral-200 bg-white p-2.5 text-neutral-600 shadow-sm transition-all duration-200 hover:border-neutral-300 hover:text-neutral-900 dark:border-neutral-700 dark:bg-neutral-800 dark:text-neutral-200 dark:hover:border-neutral-600 dark:hover:text-white"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    @click="toggleTheme"
  >
    <span class="text-lg" aria-hidden="true">{{ isDark ? '☀️' : '🌙' }}</span>
  </button>
</template>
