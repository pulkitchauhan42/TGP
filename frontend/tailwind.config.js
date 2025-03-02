module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        gold: {
          500: '#FFD700', // Define gold color at 500 shade
        },
        primary: "#0D3B25", // Dark green
        secondary: "#C0A06E", // Gold
        accent: "#E5E5E5", // Light gray for contrast
        textDark: '#333333', // Dark text color
      },
      fontFamily: {
        serif: ["Playfair Display", "serif"], // Elegant serif font
        sans: ["Poppins", "sans-serif"], // Modern, clean sans-serif
      },
    },
  },
  plugins: [],
};
