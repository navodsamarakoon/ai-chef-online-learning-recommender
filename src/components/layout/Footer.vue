<script setup lang="ts">
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="border-t border-neutral-200/80 bg-white transition-colors duration-200 dark:border-neutral-700 dark:bg-neutral-900">
    <div
      class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-5 py-8 text-center sm:flex-row sm:px-8 sm:text-left"
    >
      <p class="text-sm font-semibold tracking-tight text-neutral-900 dark:text-white">AI Chef</p>
      <p class="text-sm text-neutral-500 dark:text-neutral-400">
        &copy; {{ currentYear }} AI Chef. All rights reserved.
      </p>
    </div>
  </footer>
</template>
