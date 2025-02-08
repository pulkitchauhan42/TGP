<template>
  <div class="container mx-auto p-6 flex flex-col items-center justify-center min-h-screen">
    <div class="max-w-md w-full bg-white p-8 shadow-lg rounded-lg border border-gray-300">
      <h2 class="text-2xl font-semibold text-gray-800 text-center mb-4">Create Your Account</h2>

      <!-- Signup Form -->
      <form @submit.prevent="handleSignup" class="mt-4">
        <input type="text" v-model="fullName" placeholder="Full Name" class="input-field" required />
        <input type="email" v-model="email" placeholder="Email Address" class="input-field" required />
        <input type="password" v-model="password" placeholder="Password" class="input-field" required />
        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" class="input-field" required />

        <!-- Error Message -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <!-- Signup Button -->
        <button type="submit" class="btn-signup mt-4">Sign Up</button>
      </form>

      <!-- Redirect to Login -->
      <div class="mt-6 text-center">
        <p class="text-gray-700">Already have an account?</p>
        <router-link to="/login?userType=non-member" class="hover:underline text-blue-600">Sign In Here</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const router = useRouter();

    const fullName = ref("");
    const email = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const errorMessage = ref("");

    // Handle Signup
    const handleSignup = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = "⚠️ Passwords do not match!";
    return;
  }

  try {
    // ✅ Send form data correctly
    const formData = new URLSearchParams();
    formData.append("full_name", fullName.value);
    formData.append("email", email.value);
    formData.append("password", password.value);
    formData.append("is_member", "false"); // Default new users to non-member

    const response = await axios.post("http://localhost:8000/api/signup", formData, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    console.log("✅ Signup Success:", response.data);

    if (response.data.token) {
      // ✅ Store token in localStorage
      localStorage.setItem("authToken", response.data.token);
    }

    alert("✅ Account created successfully!");

    // ✅ Redirect to home and reload to update UI
    router.push("/");
    setTimeout(() => window.location.reload(), 500);

  } catch (error) {
    console.error("❌ Signup error:", error.response?.data || error);
    errorMessage.value = error.response?.data?.detail || "An error occurred.";
  }
};


    return {
      fullName,
      email,
      password,
      confirmPassword,
      errorMessage,
      handleSignup,
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

.btn-signup {
  @apply w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition;
}

.error-message {
  color: #dc2626;
  font-weight: 500;
  margin-top: 0.5rem;
  text-align: center;
}
</style>
