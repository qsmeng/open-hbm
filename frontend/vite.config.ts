import { fileURLToPath, URL } from 'node:url'
import { defineConfig, loadEnv } from 'vite'
import type { Plugin } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const plugins: Plugin[] = [vue()]
  
  if (mode === 'development' && env.VITE_DEVTOOLS === 'true') {
    plugins.push(vueDevTools() as Plugin<any>)
  }

  return {
    plugins,
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    optimizeDeps: {
      include: [
        'vue',
        'vue-router',
        '@vue/runtime-core',
        '@vue/reactivity',
        '@vue/shared'
      ],
      exclude: [
        'vite-plugin-vue-devtools'
      ],
      force: true,
      cacheDir: 'node_modules/.vite',
      needsInterop: []
    },
    build: {
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true,
        },
      },
      assetsInlineLimit: 4096, // 4kb以下资源内联
      chunkSizeWarningLimit: 1000, // 提高chunk大小警告阈值
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              if (id.includes('vue')) {
                return 'vue'
              }
              if (id.includes('vue-router')) {
                return 'vue-router'
              }
              return 'vendor'
            }
          },
          entryFileNames: `assets/[name].[hash].js`,
          chunkFileNames: `assets/[name].[hash].js`,
          assetFileNames: `assets/[name].[hash].[ext]`
        },
      },
    },
    server: {
      http2: true, // 启用HTTP/2
      proxy: {
        // 代理配置示例
        '/api': {
          target: 'http://localhost:3000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
  }
})
