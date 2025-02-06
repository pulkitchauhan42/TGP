<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Book Your Simulator Time</h1>

    <form @submit.prevent="submitBooking" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg">
      
      <!-- Select Date -->
      <div class="mb-4">
        <label for="date" class="block text-lg font-semibold text-gray-700 mb-1">Select Date:</label>
        <Datepicker
          v-model="booking.date"
          :min-date="new Date()" 
          :enable-time-picker="false"
          auto-apply
          class="datepicker-custom"
          @update:model-value="fetchAvailableSlots"
        />
      </div>

      <!-- Select Time -->
      <div class="mb-4">
        <label for="time" class="block text-lg font-semibold text-gray-700 mb-1">Select Time:</label>
        <select
          id="time"
          v-model="booking.time"
          class="border border-gray-300 p-2 rounded w-full text-black"
          required
        >
          <option value="" disabled>Select a time</option>
          <option v-for="option in availableTimes" :key="option" :value="option">
            {{ option }}
          </option>
        </select>
      </div>

      <!-- Select Duration -->
      <div class="mb-4">
        <label for="duration" class="block text-lg font-semibold text-gray-700 mb-1">Duration (in hours):</label>
        <select
          id="duration"
          v-model="booking.duration"
          class="border border-gray-300 p-2 rounded w-full text-black"
          required
        >
          <option value="" disabled>Select duration</option>
          <option v-for="hour in [1, 1.5, 2, 2.5, 3, 3.5, 4]" :key="hour" :value="hour">
            {{ hour }} hour{{ hour > 1 ? 's' : '' }}
          </option>
        </select>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700">
        Confirm Booking
      </button>
    </form>

    <!-- Corporate Events Note -->
    <p class="text-center text-gold text-xl font-bold mt-6">
      For corporate events, please 
      <a href="mailto:bookings@thatgolfplace.com" class="text-white underline hover:text-gray-300">email us</a> 
      or call 
      <a href="tel:6304186267" class="text-white underline hover:text-gray-300">630-418-6267</a>.
    </p>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import axios from "axios";
import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

export default {
  components: {
    Datepicker, // Register Vue3 Datepicker Component
  },
  setup() {
    const booking = ref({
      date: new Date(),
      time: "",
      duration: 1,
    });

    const availableTimes = ref([]);

    // Format date to YYYY-MM-DD before sending to backend
    const formatDate = (date) => {
      return date.toISOString().split("T")[0];
    };

    // Fetch available slots from backend and update UI
    const fetchAvailableSlots = async () => {
      if (!booking.value.date) return;
      try {
        console.log("🔄 Fetching available slots...");
        
        const formattedDate = formatDate(booking.value.date); // Format date
        const response = await axios.get(`http://localhost:8000/api/booked-slots?date=${formattedDate}`);
        
        availableTimes.value = [];
        await new Promise(resolve => setTimeout(resolve, 100)); // Small delay for reactivity
        availableTimes.value = response.data.availableSlots || [];

        console.log("✅ Updated available times:", availableTimes.value);
      } catch (error) {
        console.error("❌ Error fetching available slots:", error);
      }
    };

    // Watch for changes in date selection
    watch(() => booking.value.date, fetchAvailableSlots);

    // Submit booking
    const submitBooking = async () => {
      try {
        if (!booking.value.date || !booking.value.time || !booking.value.duration) {
          alert("Please fill out all fields.");
          return;
        }

        const formattedDate = formatDate(booking.value.date);

        const formData = new URLSearchParams();
        formData.append("date", formattedDate);
        formData.append("time", booking.value.time);
        formData.append("duration", booking.value.duration.toString());

        const response = await axios.post("http://localhost:8000/api/book", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        alert(response.data.message);

        // **Wait slightly before refreshing available slots**
        setTimeout(fetchAvailableSlots, 500);

      } catch (error) {
        console.error("Booking error:", error);
        alert(error.response?.data?.detail || "An error occurred");
      }
    };

    return {
      booking,
      availableTimes,
      fetchAvailableSlots,
      submitBooking,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
label {
  @apply text-lg font-semibold text-gray-700 block mb-1;
}
/* Ensure text inside inputs is visible */
input, select {
  @apply text-black bg-white border-gray-300 focus:border-primary focus:ring-primary focus:outline-none;
  padding: 0.5rem;
  border-radius: 0.375rem;
  width: 100%;
}
button {
  @apply w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700;
}

/* Custom styles for Datepicker */
.datepicker-custom {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem;
  background-color: white;
}
</style>
