import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0', // This allows both localhost and the 172.x IP to work
    https: false,    // FORCE DISABLE HTTPS
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
        secure: false,
        // Do NOT use a rewrite here if your backend routes already start with /api
      }
}
  }
})