/**
 * Vite配置文件
 * 老王我配好了，别tm乱改端口！
 * 优化了Windows下的进程退出处理
 */
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: false, // 端口被占用时自动尝试下一个
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    },
    // 优化文件监听，Windows下使用轮询避免句柄泄漏
    watch: {
      usePolling: false, // 默认不用轮询，性能更好
      interval: 1000
    }
  },
  // 优化依赖预构建
  optimizeDeps: {
    exclude: ['@vueup/vue-quill']
  },
  // 构建优化
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'editor': ['@vueup/vue-quill', 'dompurify']
        }
      }
    }
  }
})
