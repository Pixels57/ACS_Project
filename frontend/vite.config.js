import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Determine backend protocol from environment variable
  // USE_HTTP=true means backend runs on HTTP, otherwise HTTPS
  const useHttp = process.env.USE_HTTP === 'true' || process.env.USE_HTTP === '1'
  const backendProtocol = useHttp ? 'http' : 'https'
  const backendUrl = process.env.VITE_API_URL || `${backendProtocol}://localhost:8000`
  
  // For HTTPS: accept self-signed/trusted certificates for local development
  // If certificate is trusted in system CA store, can use secure: true
  const secure = !useHttp ? false : undefined // false = accept self-signed certs for dev
  
  // Path to backend certificate files
  const certPath = path.resolve(__dirname, '../backend/cert.pem')
  const keyPath = path.resolve(__dirname, '../backend/key.pem')
  
  // Enable HTTPS for frontend when not using HTTP mode
  let httpsConfig = undefined
  if (!useHttp) {
    // Check if certificate files exist
    if (fs.existsSync(certPath) && fs.existsSync(keyPath)) {
      httpsConfig = {
        key: fs.readFileSync(keyPath),
        cert: fs.readFileSync(certPath),
      }
      console.log(`[Frontend] HTTPS enabled using backend certificate`)
    } else {
      console.warn(`[Frontend] Certificate files not found at ${certPath}`)
      console.warn(`[Frontend] Frontend will run on HTTP (backend still uses HTTPS)`)
    }
  }
  
  console.log(`[Frontend] Proxy configured for: ${backendUrl}`)
  if (!useHttp) {
    console.log(`[Frontend] Accepting local certificate (secure: false for dev)`)
  }
  
  return {
    plugins: [react()],
    server: {
      port: 3000,
      https: httpsConfig,  // Enable HTTPS when not using HTTP mode
      proxy: {
        '/api': {
          // Proxy configuration for backend API
          // Automatically matches backend protocol (HTTP or HTTPS)
          target: backendUrl,
          changeOrigin: true,
          secure: secure,  // false = accept self-signed certificates for local dev
        }
      }
    }
  }
})

