import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all addresses
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://server:8000',
        changeOrigin: true,
        secure: false
      }
    },
    watch: {
      usePolling: true, // Better for Docker
    },
    hmr: {
      port: 5173,
      host: process.env.VITE_HMR_HOST || '0.0.0.0'
    }
  },
  optimizeDeps: {
    exclude: ['crypto']
  }
})
