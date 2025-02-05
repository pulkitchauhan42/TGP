<template>
  <div class="relative bg-cover bg-center min-h-screen" style="background-image: url('/golf-club-luxury.jpg');">
    <!-- Dark Overlay for Readability -->
    <div class="absolute inset-0 bg-black bg-opacity-50"></div>

    <div class="relative max-w-5xl mx-auto p-10 text-white text-center">
      <h1 class="text-5xl font-extrabold tracking-wide mb-6">Welcome to That Golf Place</h1>
      <p class="text-lg max-w-3xl mx-auto leading-relaxed">
        Step into a world of cutting-edge golf simulation technology, where luxury meets the love of the game.
        Whether you’re a seasoned pro or just starting out, our state-of-the-art facilities provide an experience like no other.
      </p>

      <!-- About Section -->
      <div class="mt-10 space-y-6">
        <div class="bg-white bg-opacity-10 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-semibold">The Ultimate Golfing Experience</h2>
          <p class="mt-2 text-gray-300">
            Our simulators replicate the most famous courses around the world with high-precision technology.
            Every shot, every detail, captured to perfection.
          </p>
        </div>

        <div class="bg-white bg-opacity-10 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-semibold">Luxury Meets Comfort</h2>
          <p class="mt-2 text-gray-300">
            Immerse yourself in our warm and inviting atmosphere. Leather seating, ambient lighting, and top-tier service make every session a delight.
          </p>
        </div>

        <div class="bg-white bg-opacity-10 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-semibold">Perfect for Groups & Events</h2>
          <p class="mt-2 text-gray-300">
            Whether it's a casual round with friends, a corporate event, or a private tournament, we provide an unmatched setting for any occasion.
          </p>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="mt-10">
        <router-link to="/booking">
          <button class="bg-gold text-black font-bold py-3 px-8 rounded-lg text-xl shadow-lg hover:bg-yellow-500">
            Book a Session
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bg-gold {
  background-color: #d4af37; /* Luxurious Gold */
}
</style>
