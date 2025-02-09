<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center text-gray-900 mb-6">Complete Your Payment</h1>

    <!-- Booking Summary -->
    <div class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Booking Details</h2>
      <p class="text-gray-700"><strong>Location:</strong> {{ bookingLocation }}</p>
      <p class="text-gray-700"><strong>Date:</strong> {{ bookingDate }}</p>
      <p class="text-gray-700"><strong>Time:</strong> {{ bookingTime }}</p>
      <p class="text-gray-700"><strong>Duration:</strong> {{ bookingDuration }} hour(s)</p>
      <p class="text-xl font-bold mt-4 text-gray-900">Total: ${{ totalPrice }}</p>
    </div>

    <!-- Payment Button -->
    <div v-if="!isMember" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300 mt-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Confirm Payment</h2>

      <!-- Waiver Agreement -->
      <div class="mt-4 flex items-center">
        <input type="checkbox" id="waiver" v-model="waiverAgreed" class="mr-2" />
        <label for="waiver" class="text-sm text-gray-700">
          I agree to the <a href="#" class="text-blue-600 hover:underline">waiver and terms</a>.
        </label>
      </div>

      <!-- Confirm Payment -->
      <button @click="processPayment" class="btn-confirm mt-4" :disabled="!waiverAgreed">
        Pay ${{ totalPrice }}
      </button>
    </div>

    <!-- Member Confirmation (No Payment Required) -->
    <div v-if="isMember" class="text-center mt-6">
      <p class="text-green-700 font-bold">✅ Your booking has been confirmed! No payment is required for members.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";

export default {
  setup() {

    const route = useRoute();

    const bookingLocation = ref("");
    const bookingDate = ref("");
    const bookingTime = ref("");
    const bookingDuration = ref(1);
    const totalPrice = ref(50);
    const waiverAgreed = ref(false);
    const isMember = ref(false);

    onMounted(() => {
      bookingLocation.value = route.query.location || "That Golf Place - Main Location";
      bookingDate.value = route.query.date || "";
      bookingTime.value = route.query.time || "";
      bookingDuration.value = parseFloat(route.query.duration) || 1;
      totalPrice.value = bookingDuration.value * 50;

      // Retrieve user authentication & membership status
      const token = localStorage.getItem("authToken");
      if (token) {
        axios
          .get("http://localhost:8000/api/user-status", {
            headers: { Authorization: `Bearer ${token}` },
          })
          .then((response) => {
            isMember.value = response.data.isMember;
          })
          .catch(() => {
            isMember.value = false;
          });
      }
    });

    const processPayment = async () => {
      if (!waiverAgreed.value) {
        alert("⚠️ You must agree to the waiver before proceeding.");
        return;
      }

      const userEmail = localStorage.getItem("userEmail") || ""; // Ensure email exists

      if (!userEmail) {
        alert("⚠️ Your email is missing. Please log in again.");
        return;
  }
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/create-checkout-session", {
          date: bookingDate.value,
          time: bookingTime.value,
          duration: bookingDuration.value,
          location: bookingLocation.value,
          email: userEmail, // Retrieve stored email from login
        });

        window.location.href = response.data.checkout_url; // Redirect to Stripe Checkout
      } catch (error) {
        console.error("❌ Payment error:", error);
        alert("Payment failed. Please try again.");
      }
    };

    return {
      bookingLocation,
      bookingDate,
      bookingTime,
      bookingDuration,
      totalPrice,
      waiverAgreed,
      isMember,
      processPayment,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.btn-confirm {
  @apply w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition;
}

/* Disabled Button Styling */
.btn-confirm:disabled {
  @apply bg-gray-400 cursor-not-allowed;
}

label {
  @apply text-gray-800 font-medium;
}
</style>
