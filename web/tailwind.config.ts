import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        'linkai-blue': '#2E5AAC',
        'knowledge-gray': '#F5F7FA',
      }
    },
  },
  plugins: [],
}
export default config