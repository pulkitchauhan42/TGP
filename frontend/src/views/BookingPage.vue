<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Book Your Simulator Time</h1>

    <form @submit.prevent="confirmBooking" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg">
      
      <!-- Select Location -->
      <div class="mb-4">
        <label for="location" class="block text-lg font-semibold text-gray-700 mb-1">Select Location:</label>
        <select id="location" v-model="booking.location" class="border border-gray-300 p-2 rounded w-full text-black" required>
          <option v-for="loc in locations" :key="loc" :value="loc">{{ loc }}</option>
        </select>
      </div>

      <!-- Select Date -->
      <div class="mb-4">
        <label for="date" class="block text-lg font-semibold text-gray-700 mb-1">Select Date:</label>
        <input 
          type="date" 
          id="date" 
          v-model="booking.date" 
          @change="fetchAvailableSlots" 
          :min="minDate" 
          class="border border-gray-300 p-2 rounded w-full text-black" 
          required 
        />
      </div>

      <!-- Select Time -->
      <div class="mb-4">
        <label for="time" class="block text-lg font-semibold text-gray-700 mb-1">Select Time:</label>
        <select id="time" v-model="booking.time" class="border border-gray-300 p-2 rounded w-full text-black" required>
          <option value="" disabled>Select a time</option>
          <option v-for="option in availableTimes" :key="option" :value="option">{{ option }}</option>
        </select>
      </div>

      <!-- Select Duration -->
      <div class="mb-4">
        <label for="duration" class="block text-lg font-semibold text-gray-700 mb-1">Duration (in hours):</label>
        <select id="duration" v-model="booking.duration" class="border border-gray-300 p-2 rounded w-full text-black" required>
          <option v-for="hour in [1, 1.5, 2, 2.5, 3, 3.5, 4]" :key="hour" :value="hour">
            {{ hour }} hour{{ hour > 1 ? 's' : '' }}
          </option>
        </select>
      </div>

      <!-- Show Remaining Hours for Members -->
      <p v-if="isAuthenticated && isMember" class="text-center text-green-700 font-semibold">
        You have {{ memberHours }} hours remaining.
      </p>

      <!-- Confirm Booking Button -->
      <div class="flex justify-between mt-6">
        <button @click="goBackToSelection" type="button" class="btn-back">← Back</button>
        <button type="submit" class="btn-confirm">Confirm Booking →</button>
      </div>
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
import { ref, watch, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const booking = ref({
      location: "Main Facility", 
      date: "",
      time: "",
      duration: 1,
    });

    const locations = ref(["Main Facility - 123 Golf Club Ln, Chicago, IL 60601"]);
    const availableTimes = ref([]);
    const minDate = ref(new Date().toISOString().split("T")[0]);
    const isAuthenticated = ref(false);
    const isMember = ref(false);
    const memberHours = ref(0);

    // Fetch user authentication status
    const fetchUserStatus = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) {
        isAuthenticated.value = false;
        return;
      }
      try {
        const response = await axios.get("http://localhost:8000/api/me", {
          headers: { Authorization: `Bearer ${token}` },
        });

        isAuthenticated.value = true;
        isMember.value = response.data.is_member;
        memberHours.value = response.data.member_hours;

        console.log("🟢 DEBUG: User authenticated", response.data);
      } catch (error) {
        console.error("❌ Error fetching user status:", error);
        isAuthenticated.value = false;
      }
    };

    onMounted(fetchUserStatus);

    // Fetch available slots
    const fetchAvailableSlots = async () => {
      if (!booking.value.date) return;
      try {
        const response = await axios.get(`http://localhost:8000/api/booked-slots`, {
          params: { date: booking.value.date, location: booking.value.location },
        });

        availableTimes.value = response.data.availableSlots || [];
      } catch (error) {
        console.error("❌ Error fetching available slots:", error);
      }
    };

    watch(() => booking.value.date, fetchAvailableSlots);
    watch(() => booking.value.location, fetchAvailableSlots);

    // Confirm Booking
    const confirmBooking = async () => {
  console.log("🟢 DEBUG: Confirming booking with details:", booking.value);

  if (!isAuthenticated.value) {
    console.warn("🔴 User is not authenticated! Redirecting to login...");
    router.push({
      path: "/login",
      query: { ...booking.value, userType: "non-member" },
    });
    return;
  }

  if (isMember.value) {
    if (memberHours.value < booking.value.duration) {
      alert("Not enough allocated hours. Redirecting to payment.");
      router.push({
        path: "/payment",
        query: { ...booking.value },
      });
      return;
    }
  }

  try {
    const token = localStorage.getItem("authToken");
    if (!token) {
      alert("You are not logged in. Please sign in to book.");
      return;
    }

    console.log("🟢 DEBUG: Sending booking request to backend...");

    // 🔹 Convert payload to URLSearchParams (required for FastAPI Form data)
    const requestData = new URLSearchParams();
    requestData.append("location", booking.value.location);
    requestData.append("date", booking.value.date);
    requestData.append("time", booking.value.time);
    requestData.append("duration", booking.value.duration.toString());

    console.log("📡 Sending Form Data:", requestData.toString());

    const response = await axios.post(
      "http://localhost:8000/api/book",
      requestData, // 🔹 Correct format for FastAPI Form
      { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/x-www-form-urlencoded" } }
    );

    console.log("✅ Booking success response:", response.data);
    alert(response.data.message);

    fetchUserStatus(); // Update member hours
  } catch (error) {
    console.error("❌ Booking error:", error.response?.data || error);
    alert(error.response?.data?.detail || "An error occurred while booking.");
  }
};



    return {
      booking,
      locations,
      availableTimes,
      isAuthenticated,
      isMember,
      memberHours,
      fetchAvailableSlots,
      confirmBooking,
      minDate,
    };
  },
};
</script>



<style scoped>
.container {
  max-width: 600px;
}

.btn-confirm {
  @apply bg-green-600 text-white py-3 px-6 rounded-lg text-lg font-bold hover:bg-green-700 transition;
}

.btn-back {
  @apply bg-gray-400 text-white py-3 px-6 rounded-lg text-lg font-bold hover:bg-gray-500 transition;
}
</style>
