<template>
  <div class="space-y-8" role="status" aria-live="polite" aria-label="Loading recipe details">
    <div class="overflow-hidden rounded-2xl bg-neutral-100 shadow-sm dark:bg-neutral-800">
      <div class="aspect-[16/9] w-full animate-pulse bg-neutral-200 sm:aspect-[21/9] dark:bg-neutral-700" />
    </div>

    <div class="space-y-4">
      <div class="h-8 w-2/3 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700 sm:h-10" />

      <div class="flex flex-wrap items-center gap-3">
        <div class="h-10 w-24 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        <div class="h-4 w-24 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        <div class="h-6 w-20 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        <div class="h-4 w-24 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
      </div>
    </div>

    <div class="grid gap-10 md:grid-cols-2">
      <div>
        <div class="mb-4 h-6 w-32 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        <div class="space-y-2">
          <div class="h-4 w-full animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-11/12 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-4/5 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-full animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        </div>
      </div>

      <div>
        <div class="mb-4 h-6 w-36 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        <div class="space-y-4">
          <div class="flex gap-3">
            <div class="h-6 w-6 shrink-0 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
            <div class="h-4 flex-1 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          </div>
          <div class="flex gap-3">
            <div class="h-6 w-6 shrink-0 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
            <div class="h-4 flex-1 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          </div>
          <div class="flex gap-3">
            <div class="h-6 w-6 shrink-0 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
            <div class="h-4 flex-1 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
