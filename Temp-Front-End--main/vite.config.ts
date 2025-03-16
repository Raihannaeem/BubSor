import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': { // Replace with your desired proxy path
           target: 'http://127.0.0.1:5000', // Replace with your backend API URL
           changeOrigin: true, // Needed for some cases, especially with HTTPS
           rewrite: (path) => path.replace(/^\/api/, ''), // Optional: Rewrite the path
         },
    },
    port: 5173,
    host: true,
  },
  optimizeDeps: {
    include: ['@emotion/react', '@emotion/styled', 'framer-motion']
  }
})
