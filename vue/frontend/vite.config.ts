import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import cssInjectedByJsPlugin from "vite-plugin-css-injected-by-js";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    // django-vue: css-injected-by-js
    cssInjectedByJsPlugin(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    rollupOptions: {
      // django-vue: preserve-entry-signatures
      preserveEntrySignatures: 'allow-extension', // do not remove root level exports
      input: {
        main: './src/main.ts',
        // django-vue: multi-entrypoints@1
        // We can use multiple entrypoints to aid in organization or for optimizing loading times
        packages: './src/packages.ts',
        dice3d: './src/dice3d.ts',
      },
      output: {
        // django-vue: production@1
        dir: '../../rpgdice/static/vue/frontend/',
        entryFileNames: '[name].js',
      },
    },
  }
})
