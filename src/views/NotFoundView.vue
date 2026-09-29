<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="flex min-h-[70vh] items-center justify-center px-5 py-16 sm:px-8 sm:py-24">
    <div class="w-full max-w-2xl rounded-3xl border border-neutral-200/80 bg-white p-8 text-center shadow-sm dark:border-neutral-700 dark:bg-neutral-900 sm:p-10">
      <div class="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-neutral-100 text-4xl shadow-sm dark:bg-neutral-800">
        🍽️
      </div>

      <p class="mt-8 text-7xl font-semibold tracking-tight text-neutral-900 dark:text-white sm:text-8xl">
        404
      </p>
      <h1 class="mt-4 text-2xl font-semibold tracking-tight text-neutral-900 dark:text-white sm:text-3xl">
        Page not found
      </h1>
      <p class="mx-auto mt-3 max-w-lg text-base leading-relaxed text-neutral-500 dark:text-neutral-400">
        Oops! The page you're looking for doesn't exist.
      </p>

      <div class="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
        <RouterLink
          to="/"
          class="inline-flex items-center justify-center rounded-full bg-neutral-900 px-5 py-2.5 text-sm font-medium text-white transition-colors duration-200 hover:bg-neutral-700 dark:bg-white dark:text-neutral-900 dark:hover:bg-neutral-200"
        >
          Go Home
        </RouterLink>
        <RouterLink
          to="/recipes"
          class="inline-flex items-center justify-center rounded-full border border-neutral-200 bg-white px-5 py-2.5 text-sm font-medium text-neutral-700 transition-colors duration-200 hover:border-neutral-300 hover:text-neutral-900 dark:border-neutral-700 dark:bg-neutral-900 dark:text-neutral-200 dark:hover:border-neutral-600 dark:hover:text-white"
        >
          Browse Recipes
        </RouterLink>
      </div>
    </div>
  </section>
</template>
