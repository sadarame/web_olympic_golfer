/** @type {import('tailwindcss').Config} */
export default {
  darkMode: false, // ← これで dark: バリアントが無効化される
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
};
