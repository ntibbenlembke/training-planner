/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-gray': 'var(--color-dark-gray)',
        'paper': 'var(--color-paper)',
        'blue': 'var(--color-blue)',
      },
    },
  },
  plugins: [],
} 