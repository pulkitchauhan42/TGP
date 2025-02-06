<template>
  <div>
    <header class="bg-primary py-4 shadow-md">
      <nav class="flex justify-between items-center px-8 relative">
        <h1 class="text-secondary text-3xl font-serif">That Golf Place</h1>

        <!-- Navigation Links -->
        <div class="flex space-x-6 items-center">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/booking" class="nav-link">Booking</router-link>

          <!-- Memberships Dropdown -->
          <div class="relative group">
            <button @click="toggleDropdown" class="nav-link flex items-center">
              Memberships <span class="ml-1">▼</span>
            </button>

            <!-- Dropdown Menu -->
            <div
              class="absolute left-0 mt-2 w-56 bg-white shadow-lg rounded-lg z-50"
              v-show="dropdownOpen"
              @mouseenter="cancelCloseTimer"
              @mouseleave="startCloseTimer"
            >
              <router-link to="/memberships" class="dropdown-link">Membership Overview</router-link>
              <router-link to="/memberships/individual" class="dropdown-link">Individual Memberships</router-link>
              <router-link to="/memberships/corporate" class="dropdown-link">Corporate Memberships</router-link>
              <router-link to="/memberships/seasonal" class="dropdown-link">Seasonal Memberships</router-link>
            </div>
          </div>

          <router-link to="/contact" class="nav-link">Contact</router-link>
        </div>
      </nav>
    </header>

    <main class="p-6">
      <router-view></router-view>
    </main>

    <footer class="bg-cover bg-center py-12 text-white" style="background-image: url('/public/grass-texture.jpg');">
      <div class="container mx-auto flex flex-col md:flex-row justify-between items-center px-8">
        
        <!-- Logo -->
        <div class="flex-1 flex justify-center md:justify-start">
          <img src="/public/logo.png" alt="That Golf Place Logo" class="h-16">
        </div>
        
        <!-- Address -->
        <div class="flex-1 text-center">
          <h2 class="text-xl font-bold">Visit Us</h2>
          <p>123 Golf Club Lane</p>
          <p>Chicago, IL 60601</p>
        </div>
        
        <!-- Navigation Links -->
        <div class="flex-1 flex flex-col text-center md:text-left">
          <h2 class="text-xl font-bold">Quick Links</h2>
          <router-link to="/about" class="footer-link">About</router-link>
          <router-link to="/booking" class="footer-link">Book Now</router-link>
          <router-link to="/contact" class="footer-link">Contact</router-link>
        </div>
        
        <!-- Hours & Contact -->
        <div class="flex-1 text-center md:text-left">
          <h2 class="text-xl font-bold">Hours</h2>
          <p>Mon-Sat: 9AM - 10PM</p>
          <p>Sun: 10AM - 8PM</p>
          <router-link to="/contact" class="btn mt-4 inline-block">Contact Now</router-link>
        </div>
        
        <!-- Social Media -->
        <div class="flex-1 flex flex-col items-center md:items-end">
          <h2 class="text-xl font-bold">Follow Us</h2>
          <div class="flex space-x-4 mt-2">
            <a href="https://www.tiktok.com/@that_golf_place" target="_blank" class="social-icon">
              <font-awesome-icon :icon="['fab', 'tiktok']" />
            </a>
            <a href="https://www.instagram.com" target="_blank" class="social-icon">
              <font-awesome-icon :icon="['fab', 'instagram']" />
            </a>
            <a href="https://www.facebook.com" target="_blank" class="social-icon">
              <font-awesome-icon :icon="['fab', 'facebook']" />
            </a>
            <a href="https://www.youtube.com" target="_blank" class="social-icon">
              <font-awesome-icon :icon="['fab', 'youtube']" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref } from "vue";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faTiktok, faInstagram, faFacebook, faYoutube } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// Add icons to FontAwesome library
library.add(faTiktok, faInstagram, faFacebook, faYoutube);

export default {
  components: {
    FontAwesomeIcon,
  },
  setup() {
    const dropdownOpen = ref(false);
    let closeTimer = null;

    const toggleDropdown = () => {
      dropdownOpen.value = !dropdownOpen.value;
    };

    const startCloseTimer = () => {
      closeTimer = setTimeout(() => {
        dropdownOpen.value = false;
      }, 300); // 300ms delay before closing
    };

    const cancelCloseTimer = () => {
      if (closeTimer) {
        clearTimeout(closeTimer);
      }
    };

    return {
      dropdownOpen,
      toggleDropdown,
      startCloseTimer,
      cancelCloseTimer,
    };
  },
};
</script>

<style>
.nav-link {
  @apply text-lg text-white hover:text-secondary transition duration-300;
}

.dropdown-link {
  @apply block px-4 py-2 text-black hover:bg-gray-200 transition duration-300;
}

/* Prevents dropdown from being cut off */
.absolute {
  min-width: 200px;
  white-space: nowrap;
  transform-origin: top;
}

/* Keeps dropdown open when hovered */
.opacity-0 {
  opacity: 0;
  visibility: hidden;
  transform: scale(0.95);
}

.opacity-100 {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}

.footer-link {
  @apply text-white hover:text-secondary transition duration-300 block mt-2;
}

.btn {
  @apply bg-secondary text-primary px-6 py-2 rounded-lg text-lg font-bold;
}

.btn:hover {
  @apply bg-white text-secondary shadow-lg;
}

.social-icon {
  @apply text-2xl text-white hover:text-secondary transition duration-300;
}
</style>
