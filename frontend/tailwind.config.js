/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-default': '#A3E635',
        'primary-hover': '#84CC16',
        'success': '#22C55E',
        'warning': '#F97316',
        'error': '#DC2626',
        'info': '#2563EB',
        'background-dark': '#020617',
        'background-light': '#FFFFFF',
        'text-light': '#334155',
        'text-dark': '#FFFFFF',
        'light-grey': '#CBD5E1',
        'icon-blue': '#3B82F6',
        'icon-green': '#22C55E',
        'icon-orange': '#F97316',
        'icon-purple': '#A855F7',
        'panel-dark': '#0f172a', // Slightly lighter than bg-dark for cards/panels
        'border-dark': '#334155',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      fontSize: {
        'h1': ['64px', { lineHeight: '72px', letterSpacing: '-2px', fontWeight: '700' }],
        'h2': ['56px', { lineHeight: '64px', letterSpacing: '-2px', fontWeight: '700' }],
        'h3': ['48px', { lineHeight: '56px', letterSpacing: '-1px', fontWeight: '700' }],
        'h4': ['40px', { lineHeight: '48px', letterSpacing: '-1px', fontWeight: '700' }],
        'h5': ['32px', { lineHeight: '40px', letterSpacing: '0px', fontWeight: '700' }],
        'h6': ['24px', { lineHeight: '32px', letterSpacing: '0px', fontWeight: '700' }],
        'h7': ['20px', { lineHeight: '28px', letterSpacing: '0px', fontWeight: '700' }],
        'body-large': ['18px', { lineHeight: '32px' }],
        'body-medium': ['16px', { lineHeight: '24px' }],
        'body-small': ['14px', { lineHeight: '20px' }],
        'body-xsmall': ['12px', { lineHeight: '16px' }],
      },
      letterSpacing: {
        '-2': '-0.05em',
        '-1': '-0.025em',
      }
    },
  },
  plugins: [],
}