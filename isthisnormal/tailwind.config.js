module.exports = {
    content: [
      './components/**/*.{js,vue,ts}',
      './layouts/**/*.vue',
      './pages/**/*.vue',
      './plugins/**/*.{js,ts}',
      './nuxt.config.{js,ts}',
      './app.vue'
    ],
    theme: {
      extend: {
        fontFamily: {
          sans: ['Geist', 'system-ui', 'sans-serif'],
        },
    },
    },
    plugins: [],
  }