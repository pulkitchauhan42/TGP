<template>
  <div>
    <header class="bg-primary py-4 shadow-md">
      <nav class="flex justify-between items-center px-8">
        <h1 class="text-secondary text-3xl font-serif">That Golf Place</h1>
        <div class="space-x-6">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/booking" class="nav-link">Booking</router-link>
          <router-link to="/contact" class="nav-link">Contact</router-link>
        </div>
      </nav>
    </header>

    <main class="p-6">
      <router-view></router-view>
    </main>

    <footer class="bg-secondary text-primary py-6 text-center">
      <p>&copy; 2025 That Golf Place - Premium Golf Simulation</p>
    </footer>
  </div>
</template>

<style>
.nav-link {
  @apply text-lg text-white hover:text-secondary transition duration-300;
}
</style>