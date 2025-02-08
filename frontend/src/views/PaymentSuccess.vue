<template>
  <div class="container mx-auto p-6 text-center">
    <h1 class="text-3xl font-bold text-green-600">✅ Payment Successful!</h1>
    <p class="text-gray-700 mt-4">Your booking has been confirmed.</p>

    <!-- Booking Summary -->
    <div class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300 mt-6">
      <h2 class="text-xl font-semibold text-gray-800">Booking Details</h2>
      <p class="text-gray-700"><strong>Date:</strong> {{ bookingDate }}</p>
      <p class="text-gray-700"><strong>Time:</strong> {{ bookingTime }}</p>
      <p class="text-gray-700"><strong>Duration:</strong> {{ bookingDuration }} hour(s)</p>
      <p class="text-gray-700"><strong>Location:</strong> {{ bookingLocation }}</p>
    </div>

    <!-- Buttons -->
    <div class="flex justify-center gap-4 mt-6">
      <router-link to="/" class="btn-home">🏠 Return Home</router-link>
      <router-link to="/booking" class="btn-booking">📅 Manage Booking</router-link>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

export default {
  setup() {
    
    const route = useRoute();

    const bookingLocation = ref("");
    const bookingDate = ref("");
    const bookingTime = ref("");
    const bookingDuration = ref(1);

    onMounted(() => {
        bookingLocation.value = route.query.location || "That Golf Place - Main Location";
      bookingDate.value = route.query.date || "";
      bookingTime.value = route.query.time || "";
      bookingDuration.value = parseFloat(route.query.duration) || 1;
    });

    return {
      bookingLocation,
      bookingDate,
      bookingTime,
      bookingDuration,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
.btn-home, .btn-booking {
  @apply bg-blue-600 text-white py-2 px-4 rounded-lg font-bold hover:bg-blue-700 transition;
}
</style>
