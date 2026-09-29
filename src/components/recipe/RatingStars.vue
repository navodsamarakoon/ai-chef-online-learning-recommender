<script setup lang="ts">
defineProps<{
  modelValue: number
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: number): void
}>()

function setRating(star: number): void {
  emit('update:modelValue', star)
}
</script>

<template>
  <div class="flex items-center gap-1" role="radiogroup" aria-label="Rate this recipe">
    <button
      v-for="star in [1, 2, 3, 4, 5]"
      :key="star"
      type="button"
      class="rounded-full text-2xl leading-none transition-transform duration-150 hover:scale-110 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-neutral-400 focus-visible:ring-offset-2"
      :aria-label="`Rate ${star} star${star > 1 ? 's' : ''}`"
      :aria-pressed="modelValue >= star"
      @click="setRating(star)"
    >
      <span
        :class="modelValue >= star ? 'text-amber-400' : 'text-neutral-300 dark:text-neutral-600'"
      >
        ★
      </span>
    </button>
  </div>
</template>