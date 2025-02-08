<template>
  <div class="container mx-auto p-6 flex flex-col items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white p-8 shadow-lg rounded-lg border border-gray-300">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-4">
        {{ isMember ? "TGP Membership Login" : "Public Individual Login" }}
      </h2>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin" class="mt-4">
        <input type="email" v-model="email" placeholder="Email Address" class="input-field" required />
        <input type="password" v-model="password" placeholder="Password" class="input-field" required />

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-600 text-sm mt-2">{{ errorMessage }}</p>

        <button type="submit" class="btn-login mt-4">Sign In</button>
      </form>

      <!-- Conditional Links for Members vs. Non-Members -->
      <div class="mt-6 text-center">
        <template v-if="isMember">
          <p class="text-gray-700">Not a member?</p>
          <router-link to="/memberships" class="link">Learn About Memberships</router-link>
          <p class="mt-3">or</p>
          <a @click="switchToNonMemberLogin" class="link">Sign In as a Non-Member</a>
        </template>

        <template v-else>
          <p class="text-gray-700">Don't have an account?</p>
          <router-link :to="{ path: '/signup', query: route.query }" class="link">Sign Up Here</router-link>
          <p class="mt-3">or</p>
          <a @click="switchToMemberLogin" class="link">TGP Member? Click here to sign in</a>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    const email = ref("");
    const password = ref("");
    const isMember = ref(false);
    const errorMessage = ref("");

    // Determine user type on page load
    const updateUserType = () => {
      isMember.value = route.query.userType === "member";
    };

    onMounted(updateUserType);
    
    // Watch for query changes and update UI dynamically
    watch(() => route.query.userType, updateUserType);

    // Handle switching between login types
    const switchToNonMemberLogin = () => {
      router.replace({ path: "/login", query: { ...route.query, userType: "non-member" } });
    };

    const switchToMemberLogin = () => {
      router.replace({ path: "/login", query: { ...route.query, userType: "member" } });
    };

    // Handle Login
    const handleLogin = async () => {
      try {
        // FastAPI requires 'username' instead of 'email' and form-encoded data
        const formData = new URLSearchParams();
        formData.append("username", email.value);
        formData.append("password", password.value);

        const response = await axios.post("http://localhost:8000/api/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        localStorage.setItem("authToken", response.data.access_token);
        alert("Login successful!");

        // ✅ Instead of redirecting to payment, just refresh the page
        window.location.reload();

      } catch (error) {
        console.error("❌ Login error:", error);
        errorMessage.value = error.response?.data?.detail || "Invalid credentials. Please try again.";
      }
    };

    return {
      email,
      password,
      isMember,
      handleLogin,
      switchToNonMemberLogin,
      switchToMemberLogin,
      errorMessage,
      route,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.input-field {
  @apply border border-gray-400 p-2 rounded w-full mt-3 text-gray-900 bg-white;
}

.btn-login {
  @apply w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition;
}

.link {
  @apply text-blue-600 hover:text-blue-800 font-bold cursor-pointer;
}

.text-red-600 {
  color: #dc2626;
}
</style>
