<script setup lang="ts">
import { computed } from 'vue'
import type { ToastMessage, ToastType } from '../../stores/toasts'

const props = defineProps<{
  toast: ToastMessage
}>()

const emit = defineEmits<{
  (event: 'dismiss', id: number): void
}>()

const toneStyles: Record<ToastType, string> = {
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800 dark:border-emerald-800/70 dark:bg-emerald-950/80 dark:text-emerald-200',
  error: 'border-rose-200 bg-rose-50 text-rose-800 dark:border-rose-800/70 dark:bg-rose-950/80 dark:text-rose-200',
  info: 'border-sky-200 bg-sky-50 text-sky-800 dark:border-sky-800/70 dark:bg-sky-950/80 dark:text-sky-200',
}

const toneIcon: Record<ToastType, string> = {
  success: '✓',
  error: '!',
  info: 'i',
}

const classes = computed(() => toneStyles[props.toast.type])
</script>

<template>
  <div
    class="pointer-events-auto w-full max-w-sm rounded-2xl border px-4 py-3 shadow-lg backdrop-blur transition-all duration-300 ease-out animate-in slide-in-from-right-full"
    :class="classes"
    role="status"
  >
    <div class="flex items-start gap-3">
      <div class="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-white/70 text-sm font-semibold dark:bg-neutral-900/60">
        {{ toneIcon[toast.type] }}
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-semibold">{{ toast.message }}</p>
      </div>
      <button
        type="button"
        class="rounded-full p-1 text-sm transition hover:bg-black/5 dark:hover:bg-white/10"
        aria-label="Dismiss notification"
        @click="emit('dismiss', toast.id)"
      >
        ×
      </button>
    </div>
  </div>
</template>
