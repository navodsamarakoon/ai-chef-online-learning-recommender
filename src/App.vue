<script setup lang="ts">
import { computed } from 'vue'
import { RouterView } from 'vue-router'
import Footer from './components/layout/Footer.vue'
import Navbar from './components/layout/Navbar.vue'
import Toast from './components/ui/Toast.vue'
import { useToastStore } from './stores/toasts'

const toastStore = useToastStore()
const hasToasts = computed(() => toastStore.toasts.length > 0)
</script>

<template>
  <div class="flex min-h-screen flex-col bg-neutral-50 text-neutral-900 transition-colors duration-200 dark:bg-neutral-950 dark:text-neutral-100">
    <Navbar />
    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <Transition name="page-fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>
    <Footer />

    <TransitionGroup
      v-if="hasToasts"
      tag="div"
      name="toast"
      class="pointer-events-none fixed right-4 top-6 z-[9999] flex w-[min(92vw,24rem)] flex-col gap-3 sm:right-6 sm:top-6"
    >
      <Toast
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        :toast="toast"
        @dismiss="toastStore.removeToast"
      />
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(1rem);
}

.toast-enter-to,
.toast-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: opacity 0.2s ease;
}

.page-fade-enter-from,
.page-fade-leave-to {
  opacity: 0;
}
</style>
