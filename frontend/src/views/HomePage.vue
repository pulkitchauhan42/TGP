<template>
  <div class="text-center">
    <!-- Hero Section -->
    <div class="relative w-full h-[500px]">
      <img src="/golf-simulator.jpg" class="absolute inset-0 w-full h-full object-cover brightness-50">
      <div class="absolute inset-0 flex flex-col items-center justify-center text-white">
        <h1 class="text-5xl font-bold text-white drop-shadow-lg">Welcome to That Golf Place</h1>
        <p class="mt-4 text-lg max-w-lg mx-auto">A premium automated golf simulator experience, designed for the modern golfer.</p>
        <router-link to="/booking"
          class="mt-6 bg-transparent text-white border-2 border-white py-3 px-6 rounded-lg text-lg font-semibold hover:bg-white hover:text-black transition duration-300">
          Book a Session
        </router-link>
      </div>
    </div>

    <!-- Features Section -->
    <section class="container mx-auto mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 px-4">
      <div class="bg-white shadow-xl rounded-lg p-6 text-center hover:shadow-2xl transition duration-300 ease-in-out">
        <font-awesome-icon :icon="['fas', 'golf-ball']" class="text-4xl text-primary mb-4"/>
        <h3 class="text-xl font-semibold text-primary">State-of-the-Art Simulators</h3>
        <p class="mt-2 text-textDark">Experience realistic golf simulations with industry-leading technology.</p>
      </div>
      <div class="bg-white shadow-xl rounded-lg p-6 text-center hover:shadow-2xl transition duration-300 ease-in-out">
        <font-awesome-icon :icon="['fas', 'cogs']" class="text-4xl text-primary mb-4"/>
        <h3 class="text-xl font-semibold text-primary">Fully Automated</h3>
        <p class="mt-2 text-textDark">Book, pay, and receive access details all online for a seamless experience.</p>
      </div>
      <div class="bg-white shadow-xl rounded-lg p-6 text-center hover:shadow-2xl transition duration-300 ease-in-out">
        <font-awesome-icon :icon="['fas', 'couch']" class="text-4xl text-primary mb-4"/>
        <h3 class="text-xl font-semibold text-primary">Luxury Environment</h3>
        <p class="mt-2 text-textDark">Relax in a private, upscale golf simulator experience, designed for your comfort.</p>
      </div>
    </section>
  </div>
</template>


<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import { faGolfBall, faCogs, faCouch } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(faGolfBall, faCogs, faCouch);

export default {
  components: {
    FontAwesomeIcon,
  },
};
</script>

<style scoped>
/* Hero Section Styles */
.text-white {
  color: white;
}

.bg-transparent {
  background-color: transparent;
}

.bg-white {
  background-color: white;
}

.text-primary {
  color: #1e1e1e; /* Dark primary color */
}

.text-textDark {
  color: #333; /* Lighter dark text color */
}

.hover\:bg-white:hover {
  background-color: white;
}

.hover\:text-black:hover {
  color: black;
}

.text-shadow {
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
}

/* Features Section */
.container {
  max-width: 1200px;
  margin: auto;
}

.card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.shadow-xl {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.text-xl {
  font-size: 1.25rem;
}

.font-semibold {
  font-weight: 600;
}

.text-4xl {
  font-size: 2.25rem;
}

/* Hover effects */
.transition {
  transition: all 0.3s ease;
}

.ease-in-out {
  transition-timing-function: ease-in-out;
}

/* Icons */
.fas {
  font-size: 2.5rem;
}
</style>
