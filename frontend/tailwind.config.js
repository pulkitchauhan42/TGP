module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0D3B25", // Dark green
        secondary: "#C0A06E", // Gold
        accent: "#E5E5E5", // Light gray for contrast
        gold: "#C0A06E",
      },
      fontFamily: {
        serif: ["Playfair Display", "serif"], // Elegant serif font
        sans: ["Poppins", "sans-serif"], // Modern, clean sans-serif
      },
    },
  },
  plugins: [],
};
