import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    outDir: '../static/js',
    emptyOutDir: true,
    lib: {
      entry: resolve(__dirname, 'src/main.ts'),
      name: 'KarmaApp',
      fileName: 'main',
      formats: ['iife']
    },
    rollupOptions: {
      output: {
        extend: true,
        globals: {
          vue: 'Vue'
        }
      }
    }
  },
  server: {
    port: 3000,
    cors: true
  }
})

