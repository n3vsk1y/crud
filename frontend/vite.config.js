import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Указываем, чтобы сервер был доступен на всех интерфейсах
    port: 5173,        // Убедитесь, что порт совпадает с тем, что указан в Dockerfile и docker-compose.yml
  },
})
