/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/**/*.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // 👈 Must include .vue files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
// /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: [
//     "./index.html",
//     "./src/**/*.{vue,js,ts,jsx,tsx}",
//   ],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }
