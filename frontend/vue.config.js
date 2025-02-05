const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    proxy: {
      '/api': { // Only proxy API requests, NOT static files
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },

  css: {
    loaderOptions: {
      postcss: {
        postcssOptions: {
          plugins: [
            require("tailwindcss"),
            require("autoprefixer"),
          ],
        },
      },
    },
  },
});
