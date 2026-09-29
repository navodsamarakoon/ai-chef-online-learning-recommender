import { defineStore } from 'pinia'
import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info'

export interface ToastMessage {
  id: number
  type: ToastType
  message: string
}

export const useToastStore = defineStore('toasts', () => {
  const toasts = ref<ToastMessage[]>([])
  let nextId = 0

  function removeToast(id: number): void {
    toasts.value = toasts.value.filter((toast) => toast.id !== id)
  }

  function showToast(message: string, type: ToastType = 'info', duration = 3000): void {
    const id = ++nextId

    toasts.value = [...toasts.value, { id, type, message }]

    setTimeout(() => {
      removeToast(id)
    }, duration)
  }

  return {
    toasts,
    removeToast,
    showToast,
  }
})
