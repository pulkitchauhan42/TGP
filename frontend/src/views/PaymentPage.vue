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

    <!-- Payment Form -->
    <form v-if="!isMember" @submit.prevent="submitPayment" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300 mt-6">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Payment Details</h2>

      <!-- User Info (For Receipt) -->
      <input type="email" v-model="userEmail" placeholder="Email Address" class="input-field" required />
      <input type="text" v-model="userName" placeholder="Full Name" class="input-field" required />

      <!-- Payment Details -->
      <input type="text" placeholder="Card Number" class="input-field" required />
      <input type="text" placeholder="MM/YY" class="input-field" required />
      <input type="text" placeholder="CVC" class="input-field" required />

      <!-- Waiver Agreement -->
      <div class="mt-4 flex items-center">
        <input type="checkbox" id="waiver" v-model="waiverAgreed" class="mr-2" />
        <label for="waiver" class="text-sm text-gray-700">
          I agree to the <a href="#" class="text-blue-600 hover:underline">waiver and terms</a>.
        </label>
      </div>

      <!-- Confirm Payment -->
      <button type="submit" class="btn-confirm mt-4" :disabled="!waiverAgreed">
        Pay ${{ totalPrice }}
      </button>
    </form>

    <!-- If user is a member, show confirmation instead of payment form -->
    <div v-if="isMember" class="text-center mt-6">
      <p class="text-green-700 font-bold">✅ Your booking has been confirmed! No payment is required for members.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    const bookingLocation = ref("");
    const bookingDate = ref("");
    const bookingTime = ref("");
    const bookingDuration = ref(1);
    const totalPrice = ref(50);
    const waiverAgreed = ref(false);
    const userEmail = ref("");
    const userName = ref("");
    const isMember = ref(false); // Track membership status

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

    const submitPayment = async () => {
      if (!waiverAgreed.value) {
        alert("⚠️ You must agree to the waiver before proceeding.");
        return;
      }

      console.log("✅ Payment Successful! Redirecting...");

      // Send Receipt Email
      // try {
      //  await axios.post("http://localhost:8000/api/send-receipt", new URLSearchParams({
      //    email: userEmail.value,
      //    name: userName.value,
      //    location: bookingLocation.value,
      //    date: bookingDate.value,
      //    time: bookingTime.value,
      //    duration: bookingDuration.value.toString(),
      //    total: totalPrice.value.toString(),
      //  }));
      //  console.log("📧 Receipt email sent!");
      ///} catch (error) {
      //  console.error("❌ Error sending receipt email:", error);
      // }

      // Redirect to Payment Success Page
      router.push({
        path: "/payment-success",
        query: {
          location: bookingLocation.value,
          date: bookingDate.value,
          time: bookingTime.value,
          duration: bookingDuration.value,
        },
      });
    };

    return {
      bookingLocation,
      bookingDate,
      bookingTime,
      bookingDuration,
      totalPrice,
      waiverAgreed,
      userEmail,
      userName,
      isMember,
      submitPayment,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}

.input-field {
  @apply border border-gray-400 p-2 rounded w-full mt-2 text-gray-900 bg-white;
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
