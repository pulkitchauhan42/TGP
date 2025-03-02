<template>
  <div>
    <!-- ✅ Header -->
    <header class="bg-primary bg-opacity-10 backdrop-blur-md py-6 fixed top-0 left-0 w-full z-50 transition-all duration-300">
      <nav class="flex justify-between items-center px-8 relative">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3">
          <img src="/logo.png" alt="That Golf Place Logo" class="h-20"> <!-- Adjusted logo size -->
          <h1 class="text-white text-3xl font-serif font-semibold">That Golf Place</h1> <!-- Adjusted font size -->
        </router-link>

        <!-- Navigation Links -->
        <div class="flex space-x-6 items-center">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/booking" class="nav-link">Booking</router-link>

          <!-- Membership Dropdown -->
          <div class="relative" v-click-outside="closeDropdown">
            <button class="nav-link flex items-center text-white" @click="() =>toggleDropdown('membership')">
              Memberships <span class="ml-1">▼</span>
            </button>
            <div v-if="activeDropdown === 'membership'" class="dropdown-menu" @mouseleave="closeDropdown">
              <router-link to="/memberships" class="dropdown-link">Membership Overview</router-link>
              <router-link to="/memberships/individual" class="dropdown-link">Individual</router-link>
              <router-link to="/memberships/corporate" class="dropdown-link">Corporate</router-link>
              <router-link to="/memberships/seasonal" class="dropdown-link">Seasonal</router-link>
            </div>
          </div>

          <!-- User Account Dropdown -->
          <div class="relative" v-if="isAuthenticated" v-click-outside="closeDropdown" @mouseleave="closeDropdown">
            <button class="nav-link flex items-center text-white" @click="() => toggleDropdown('account')">
              {{ fullName || "Account" }} <span class="ml-1">▼</span>
            </button>
            <div v-if="activeDropdown === 'account'" class="dropdown-menu">
              <p v-if="user.is_member" class="p-3 text-green-600 font-semibold border-b">
                <strong>Remaining Hours:</strong> {{ user.member_hours }} hrs
              </p>
              <router-link to="/manage-bookings" class="dropdown-link">Manage Bookings</router-link>
              <router-link to="/account-settings" class="dropdown-link">Account Settings</router-link>
              <button @click="logout" class="dropdown-link text-red-600">Log Out</button>
            </div>
          </div>

          <!-- Sign In Button if Not Logged In -->
          <router-link v-else to="/login" class="nav-link text-white">Sign In</router-link>
        </div>
      </nav>
    </header>

    <!-- ✅ Main Content -->
    <main class="pt-24 p-8">
      <router-view @profileUpdated="fetchUserData" />
    </main>

    <!-- ✅ Footer - Compact and Improved -->
    <footer class="bg-primary bg-opacity-90 text-white py-6">
      <div class="max-w-5xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-center md:text-left">
        <!-- Left: Logo and Address -->
        <div class="flex flex-col items-center md:items-start space-y-2">
          <router-link to="/" class="flex items-center space-x-3">
            <img src="/logo.png" alt="That Golf Place Logo" class="h-14">
            <h1 class="text-secondary text-2xl font-serif font-semibold">That Golf Place</h1>
          </router-link>
          <p class="text-sm">123 Golf Club Ln, Chicago, IL 60601</p>
          <p class="text-sm">(123) 456-7890 | contact@thatgolfplace.com</p>
        </div>

        <!-- Middle: Quick Links -->
        <div class="flex flex-col space-y-2 mt-4 md:mt-0">
          <h3 class="text-lg font-bold">Quick Links</h3>
          <router-link to="/" class="text-white hover:text-gray-300 text-sm">Home</router-link>
          <router-link to="/about" class="text-white hover:text-gray-300 text-sm">About</router-link>
          <router-link to="/booking" class="text-white hover:text-gray-300 text-sm">Booking</router-link>
          <router-link to="/memberships" class="text-white hover:text-gray-300 text-sm">Memberships</router-link>
          <router-link to="/contact" class="text-white hover:text-gray-300 text-sm">Contact</router-link>
        </div>

        <!-- Right: Social Icons with Fixed Links -->
        <div class="flex space-x-4 mt-4 md:mt-0">
          <a href="https://www.facebook.com" target="_blank" class="social-icon" aria-label="Facebook">
            <font-awesome-icon :icon="['fab', 'facebook-f']" />
          </a>
          <a href="https://www.x.com" target="_blank" class="social-icon" aria-label="xTwitter">
            <font-awesome-icon :icon="['fab', 'x-twitter']" />
          </a>
          <a href="https://www.instagram.com" target="_blank" class="social-icon" aria-label="Instagram">
            <font-awesome-icon :icon="['fab', 'instagram']" />
          </a>
          <a href="https://www.tiktok.com" target="_blank" class="social-icon" aria-label="TikTok">
            <font-awesome-icon :icon="['fab', 'tiktok']" />
          </a>
          <a href="https://www.youtube.com" target="_blank" class="social-icon" aria-label="YouTube">
            <font-awesome-icon :icon="['fab', 'youtube']" />
          </a>
        </div>
      </div>
    </footer>
  </div>
</template>


<script>
import { library } from "@fortawesome/fontawesome-svg-core";
import { faFacebookF, faInstagram, faTiktok, faYoutube, faXTwitter } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faFacebookF, faInstagram, faTiktok, faYoutube, faXTwitter);

export default {
  components: { FontAwesomeIcon },
  data() {
    return {
      activeDropdown: null,
      isAuthenticated: false,
      fullName: '',
      user: {}
    };
  },
  methods: {
    toggleDropdown(menu) {
      this.activeDropdown = this.activeDropdown === menu ? null : menu;
    },
    closeDropdown(menu) {
      this.activeDropdown = menu;
    },
    async fetchUserData() {
      const token = localStorage.getItem("authToken");
      if (!token) {
        this.isAuthenticated = false;
        return;
      }
      try {
        const response = await fetch("http://127.0.0.1:8000/api/me", {
          method: "GET",
          headers: { Authorization: `Bearer ${token}` },
        });
        const userData = await response.json();
        if (response.ok) {
          this.fullName = userData.full_name || "Account"; 
          this.user = userData;
          this.isAuthenticated = true;
        } else {
          this.isAuthenticated = false;
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
        this.isAuthenticated = false;
      }
    }
  },
  mounted() {
    this.fetchUserData(); // Fetch user info when component loads
  }
};
</script>


<style scoped>
.nav-link {
  @apply text-white hover:text-primary transition font-medium;
}

.dropdown-menu {
  @apply absolute right-0 bg-gray-800 text-white shadow-lg rounded-lg mt-2 py-2 w-48;
}

.dropdown-link {
  @apply block px-4 py-2 hover:bg-gray-600;
}

.footer-link:hover {
  @apply text-primary;
}

.social-icon {
  @apply text-gray-400 hover:text-white transition;
}
</style>
