/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-default': '#FFFFFF',
        'primary-hover': '#E5E7EB',
        'success': '#22C55E',
        'warning': '#F97316',
        'error': '#EF4444',
        'info': '#3B82F6',
        'background-dark': '#450A0A', // Red 950
        'background-light': '#FFFFFF',
        'text-light': '#B91C1C', // Red 700
        'text-dark': '#FFFFFF',
        'light-grey': '#FECACA', // Red 200
        'icon-blue': '#FFFFFF',
        'icon-green': '#FFFFFF',
        'icon-orange': '#FFFFFF',
        'icon-purple': '#FFFFFF',
        'panel-dark': '#7F1D1D', // Red 900
        'border-dark': '#FECACA', // Red 200
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