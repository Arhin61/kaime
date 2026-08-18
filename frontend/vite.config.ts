import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    // The API and the SPA share the /dashboard prefix, so during `npm run dev`
    // these paths must reach the backend instead of the dev server's SPA
    // fallback. Only XHR/fetch requests are proxied; browser navigations still
    // fall through to index.html so client-side routing keeps working.
    proxy: {
      '^/(dashboard|internal|docs|openapi.json)': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        bypass: (req) =>
          req.headers.accept?.includes('text/html') ? '/index.html' : undefined,
      },
    },
  },
})
