<template>
  <div class="text-center">
    <!-- Hero Section -->
    <div class="relative w-full h-[500px]">
      <img src="/golf-simulator.jpg" class="absolute inset-0 w-full h-full object-cover brightness-75">
      <div class="absolute inset-0 flex flex-col items-center justify-center text-textLight">
        <h1 class="text-5xl font-serif font-bold text-secondary">Welcome to That Golf Place</h1>
        <p class="mt-4 text-lg">A premium automated golf simulator experience</p>
        <router-link to="/booking"
          class="mt-6 bg-secondary text-textDark py-3 px-6 rounded-lg text-lg font-bold hover:bg-gold-500 transition">
          Book a Session
        </router-link>
      </div>
    </div>

    <!-- Features Section -->
    <section class="container mx-auto mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white shadow-lg rounded-lg p-6 text-center">
        <h3 class="text-xl font-serif font-bold text-primary">State-of-the-Art Simulators</h3>
        <p class="mt-2 text-textDark">Experience realistic golf simulations with industry-leading technology.</p>
      </div>
      <div class="bg-white shadow-lg rounded-lg p-6 text-center">
        <h3 class="text-xl font-serif font-bold text-primary">Fully Automated</h3>
        <p class="mt-2 text-textDark">Book, pay, and receive access details all online.</p>
      </div>
      <div class="bg-white shadow-lg rounded-lg p-6 text-center">
        <h3 class="text-xl font-serif font-bold text-primary">Luxury Environment</h3>
        <p class="mt-2 text-textDark">Relax in a premium, private golf simulator experience.</p>
      </div>
    </section>
  </div>
</template>
