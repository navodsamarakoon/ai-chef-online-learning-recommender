import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  server: {
    watch: {
      // Prevent Vite from reloading the page every time the Python
      // backend writes interaction data to backend/data/interactions.json.
      // Without this, every view/rating/favorite event triggers a
      // full-page reload loop.
      ignored: ['**/backend/**'],
    },
  },
})