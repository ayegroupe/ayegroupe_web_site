/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        brand: {
          navy: '#0A192F',
          'navy-dark': '#060D19',
          'navy-light': '#122646',
          blue: '#2563EB',
          'blue-dark': '#1D4ED8',
          'blue-light': '#60A5FA',
          gold: '#F59E0B',
          'gold-dark': '#D97706',
          'gold-light': '#FBBF24',
          emerald: '#10B981',
          'emerald-dark': '#059669',
          slate: '#0F172A',
          surface: '#F8FAFC',
          muted: '#64748B',
        },
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
        display: ['"Plus Jakarta Sans"', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glow-blue': '0 0 25px -5px rgba(37, 99, 235, 0.35)',
        'glow-gold': '0 0 25px -5px rgba(245, 158, 11, 0.35)',
        'card-hover': '0 20px 35px -5px rgba(10, 25, 47, 0.12), 0 10px 10px -5px rgba(37, 99, 235, 0.05)',
      },
    },
  },
  plugins: [],
};
