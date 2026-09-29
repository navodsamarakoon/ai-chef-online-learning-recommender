<template>
  <div class="relative">
    <div class="overflow-hidden rounded-2xl border border-neutral-200/80 bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-900">
      <div class="aspect-[4/3] overflow-hidden bg-neutral-100 dark:bg-neutral-800">
        <div class="h-full w-full animate-pulse bg-neutral-200 dark:bg-neutral-700" />
      </div>

      <div class="space-y-3 p-5">
        <div class="space-y-2">
          <div class="h-6 w-3/4 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-1/3 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <div class="h-7 w-20 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-24 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-4 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
          <div class="h-4 w-24 animate-pulse rounded-full bg-neutral-200 dark:bg-neutral-700" />
        </div>
      </div>
    </div>

    <div class="absolute right-3 top-3 h-10 w-10 animate-pulse rounded-full border border-white/80 bg-white/90 dark:border-neutral-700 dark:bg-neutral-800/90" />
  </div>
</template>
