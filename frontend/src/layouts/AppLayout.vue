<template>
  <div>
    <!-- ✅ Header -->
    <header class="bg-primary bg-opacity-10 backdrop-blur-md py-4 shadow-md fixed top-0 left-0 w-full z-50 transition duration-300">
      <nav class="flex justify-between items-center px-8 relative">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-3">
          <img src="/logo.png" alt="That Golf Place Logo" class="h-12">
          <h1 class="text-secondary text-3xl font-serif">That Golf Place</h1>
        </router-link>

        <!-- Navigation Links -->
        <div class="flex space-x-6 items-center">
          <router-link to="/" class="nav-link">Home</router-link>
          <router-link to="/about" class="nav-link">About</router-link>
          <router-link to="/booking" class="nav-link">Booking</router-link>

          <!-- Memberships Dropdown -->
          <div class="relative" @mouseleave="closeDropdown">
            <button @click="toggleDropdown('membership')" class="nav-link flex items-center">
              Memberships <span class="ml-1">▼</span>
            </button>
            <div v-if="activeDropdown === 'membership'" class="dropdown-menu">
              <router-link to="/memberships" class="dropdown-link">Membership Overview</router-link>
              <router-link to="/memberships/individual" class="dropdown-link">Individual Memberships</router-link>
              <router-link to="/memberships/corporate" class="dropdown-link">Corporate Memberships</router-link>
              <router-link to="/memberships/seasonal" class="dropdown-link">Seasonal Memberships</router-link>
            </div>
          </div>

          <!-- User Account Dropdown -->
          <div class="relative" v-if="isAuthenticated" @mouseleave="closeDropdown">
            <button @click="toggleDropdown('account')" class="nav-link flex items-center">
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

          <!-- Show Sign In Button if Not Logged In -->
          <router-link v-else to="/login" class="nav-link">Sign In</router-link>
        </div>
      </nav>
    </header>

    <!-- ✅ Main Content -->
    <main class="pt-20 p-6">
      <router-view @profileUpdated="fetchUserData" />
    </main>

    <!-- ✅ Footer with Grass Background & Social Links -->
    <footer class="relative text-white">
      <!-- Background Image -->
      <img src="/grass.png" alt="Grass Background" class="absolute inset-0 w-full h-full object-cover" />

      <!-- Footer Content -->
      <div class="relative z-10 max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center p-6">
        <div class="text-center md:text-left">
          <h2 class="text-xl font-bold">That Golf Place</h2>
          <p class="text-sm">© {{ new Date().getFullYear() }} All Rights Reserved.</p>
        </div>

        <div class="flex space-x-6 mt-4 md:mt-0">
          <a href="https://facebook.com" target="_blank" class="social-icon">🔵 Facebook</a>
          <a href="https://twitter.com" target="_blank" class="social-icon">🔷 Twitter</a>
          <a href="https://instagram.com" target="_blank" class="social-icon">📸 Instagram</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, watchEffect } from "vue";
import axios from "axios";

export default {
  setup() {
    const isAuthenticated = ref(false);
    const user = ref({ email: "", is_member: false, member_hours: 0 });
    const fullName = ref(localStorage.getItem("fullName") || "Account");
    const activeDropdown = ref(null);

    // Fetch user details
    const fetchUserData = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) return;

      try {
        const response = await axios.get("http://localhost:8000/api/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        user.value = response.data;
        isAuthenticated.value = true;
        fullName.value = response.data.full_name || "Account";
      } catch (error) {
        console.error("Error fetching user data:", error);
        isAuthenticated.value = false;
      }
    };

    // ✅ Automatically detect authentication state change
    watchEffect(() => {
      if (localStorage.getItem("authToken")) {
        fetchUserData();
      }
    });

    // Toggle dropdown visibility
    const toggleDropdown = (dropdown) => {
      activeDropdown.value = activeDropdown.value === dropdown ? null : dropdown;
    };

    // Close dropdowns
    const closeDropdown = () => {
      activeDropdown.value = null;
    };

    // Logout function
    const logout = () => {
      localStorage.removeItem("authToken");
      localStorage.removeItem("fullName");
      isAuthenticated.value = false;
      fullName.value = "Account";
      window.location.reload();
    };

    onMounted(fetchUserData);

    return {
      isAuthenticated,
      user,
      fullName,
      logout,
      activeDropdown,
      toggleDropdown,
      closeDropdown,
      fetchUserData, // ✅ Expose fetchUserData for dynamic updates
    };
  },
};
</script>

<style scoped>
/* ✅ Navigation Styling */
.nav-link {
  @apply text-lg text-white hover:text-secondary transition duration-300;
}

/* ✅ Dropdown Menu */
.dropdown-menu {
  @apply absolute right-0 mt-2 w-56 bg-white shadow-lg rounded-lg z-50 transition-opacity duration-300;
}

/* ✅ Dropdown Links */
.dropdown-link {
  @apply block px-4 py-2 text-black hover:bg-gray-200 transition duration-300;
}

/* ✅ Footer */
footer {
  height: 200px; /* Ensures proper height */
  width: 100%;
  position: relative;
  overflow: hidden;
}

/* ✅ Social Media Icons */
.social-icon {
  @apply text-lg font-semibold hover:text-gray-300 transition duration-300;
}
</style>
