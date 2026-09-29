<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import ThemeToggle from '../ui/ThemeToggle.vue'

interface NavItem {
  label: string
  to: string
  name: string
}

const navItems: NavItem[] = [
  { label: 'Home', to: '/', name: 'home' },
  { label: 'Recipes', to: '/recipes', name: 'recipes' },
  { label: 'Recommendations', to: '/recommendations', name: 'recommendations' },
  { label: 'Favorites', to: '/favorites', name: 'favorites' },
]

const route = useRoute()
const isMenuOpen = ref(false)
const menuButton = ref<HTMLButtonElement | null>(null)
const menuPanel = ref<HTMLElement | null>(null)

function toggleMenu(): void {
  isMenuOpen.value = !isMenuOpen.value
}

function closeMenu(): void {
  isMenuOpen.value = false
}

function handleClickOutside(event: MouseEvent): void {
  const target = event.target as Node | null

  if (!target) {
    return
  }

  const clickedInsideMenu = menuPanel.value?.contains(target) ?? false
  const clickedButton = menuButton.value?.contains(target) ?? false

  if (!clickedInsideMenu && !clickedButton && isMenuOpen.value) {
    closeMenu()
  }
}

function handleResize(): void {
  if (window.innerWidth >= 768) {
    closeMenu()
  }
}

watch(
  () => route.fullPath,
  () => {
    closeMenu()
  },
)

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})

function isActive(name: string): boolean {
  return route.name === name
}
</script>

<template>
  <header class="sticky top-0 z-50 border-b border-neutral-200/80 bg-white/80 backdrop-blur-md dark:border-neutral-700 dark:bg-neutral-900/80">
    <nav class="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
      <RouterLink
        to="/"
        class="text-lg font-semibold tracking-tight text-neutral-900 transition-colors duration-200 hover:text-neutral-600 dark:text-white dark:hover:text-neutral-300"
        @click="closeMenu"
      >
        AI Chef
      </RouterLink>

      <ul class="hidden items-center gap-8 md:flex">
        <li v-for="item in navItems" :key="item.name">
          <RouterLink
            :to="item.to"
            class="text-sm font-medium transition-colors duration-200"
            :class="
              isActive(item.name)
                ? 'text-neutral-900 dark:text-white'
                : 'text-neutral-500 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white'
            "
          >
            {{ item.label }}
          </RouterLink>
        </li>
      </ul>

      <div class="flex items-center gap-2">
        <div class="hidden md:flex">
          <ThemeToggle />
        </div>
        <button
          ref="menuButton"
          type="button"
          class="inline-flex h-11 w-11 items-center justify-center rounded-xl border border-neutral-200 bg-white/90 text-neutral-700 shadow-sm transition-all duration-200 hover:bg-neutral-100 dark:border-neutral-700 dark:bg-neutral-800/90 dark:text-neutral-200 dark:hover:bg-neutral-700 md:hidden"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          :aria-label="isMenuOpen ? 'Close navigation menu' : 'Open navigation menu'"
          @click.stop="toggleMenu"
        >
          <span class="flex flex-col items-center justify-center gap-1.5">
            <span
              class="block h-0.5 w-5 rounded-full bg-current transition-all duration-300"
              :class="isMenuOpen ? 'translate-y-2 rotate-45' : ''"
            ></span>
            <span
              class="block h-0.5 w-5 rounded-full bg-current transition-all duration-300"
              :class="isMenuOpen ? 'opacity-0' : 'opacity-100'"
            ></span>
            <span
              class="block h-0.5 w-5 rounded-full bg-current transition-all duration-300"
              :class="isMenuOpen ? '-translate-y-2 -rotate-45' : ''"
            ></span>
          </span>
        </button>
      </div>
    </nav>

    <Transition name="mobile-menu">
      <div
        v-if="isMenuOpen"
        ref="menuPanel"
        id="mobile-menu"
        class="border-t border-neutral-200/80 bg-white/95 px-5 py-4 shadow-sm dark:border-neutral-700 dark:bg-neutral-900/95 md:hidden"
      >
        <ul class="flex flex-col gap-1.5">
          <li v-for="item in navItems" :key="item.name">
            <RouterLink
              :to="item.to"
              class="flex items-center rounded-xl px-4 py-3 text-sm font-medium transition-colors duration-200"
              :class="
                isActive(item.name)
                  ? 'bg-neutral-100 text-neutral-900 dark:bg-neutral-800 dark:text-white'
                  : 'text-neutral-600 hover:bg-neutral-50 hover:text-neutral-900 dark:text-neutral-300 dark:hover:bg-neutral-800 dark:hover:text-white'
              "
              @click="closeMenu"
            >
              {{ item.label }}
            </RouterLink>
          </li>
        </ul>

        <div class="mt-4 rounded-xl border border-neutral-200 bg-neutral-50/80 px-4 py-3 dark:border-neutral-700 dark:bg-neutral-800/80">
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="text-sm font-medium text-neutral-900 dark:text-white">Theme</p>
              <p class="text-xs text-neutral-500 dark:text-neutral-400">Switch between light and dark</p>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.25s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-0.75rem);
}

.mobile-menu-enter-to,
.mobile-menu-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
