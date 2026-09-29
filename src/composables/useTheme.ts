import { computed, ref } from 'vue'

export type ThemeMode = 'light' | 'dark'

const STORAGE_KEY = 'ai-chef-theme'
const theme = ref<ThemeMode>('light')

function getSystemTheme(): ThemeMode {
  if (typeof window === 'undefined') {
    return 'light'
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function applyTheme(nextTheme: ThemeMode): void {
  theme.value = nextTheme

  if (typeof document === 'undefined' || typeof window === 'undefined') {
    return
  }

  document.documentElement.classList.toggle('dark', nextTheme === 'dark')
  document.documentElement.setAttribute('data-theme', nextTheme)
  window.localStorage.setItem(STORAGE_KEY, nextTheme)
}

export function initializeTheme(): void {
  if (typeof window === 'undefined') {
    return
  }

  const storedTheme = window.localStorage.getItem(STORAGE_KEY)
  const initialTheme = storedTheme === 'dark' || storedTheme === 'light' ? storedTheme : getSystemTheme()

  applyTheme(initialTheme)
}

export function useTheme() {
  const isDark = computed(() => theme.value === 'dark')

  function toggleTheme(): void {
    applyTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  return {
    theme,
    isDark,
    toggleTheme,
    initializeTheme,
  }
}
