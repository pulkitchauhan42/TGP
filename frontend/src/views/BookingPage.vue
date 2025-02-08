<template>
  <div class="container mx-auto p-6">

    <!-- Member vs. Non-Member Selection Modal -->
    <div v-if="showMemberModal" class="modal-overlay">
      <div class="modal-content">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Are you a member?</h2>
        <p class="text-gray-600 mb-6">Members can book without payment. Non-members must pay after booking.</p>

        <div class="flex flex-col gap-4 w-full">
          <button @click="selectMember(true)" class="btn-member">I’m a Member</button>
          <button @click="selectMember(false)" class="btn-non-member">I’m Not a Member</button>
        </div>
      </div>
    </div>

    <!-- Booking Form (Shows only if membership selection is completed) -->
    <form v-if="!showMemberModal" @submit.prevent="submitBooking" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg">
      
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
        <input type="date" id="date" v-model="booking.date" @change="fetchAvailableSlots" :min="minDate" class="border border-gray-300 p-2 rounded w-full text-black" required />
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
          <option v-for="hour in [1, 1.5, 2, 2.5, 3, 3.5, 4]" :key="hour" :value="hour">{{ hour }} hour{{ hour > 1 ? 's' : '' }}</option>
        </select>
      </div>

      <!-- Buttons: Confirm Booking & Back to Member Selection -->
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
import { ref, watch } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const booking = ref({
      location: "Main Facility",  // Default location
      date: "",
      time: "",
      duration: 1,
    });

    const locations = ref(["Main Facility - 123 Golf Club Ln, Chicago, IL 60601"]); // Expandable Locations ADD MORE LOCS HERE
    const availableTimes = ref([]);
    const showMemberModal = ref(true);
    const isMember = ref(null);
    const minDate = ref(new Date().toISOString().split("T")[0]);

    const selectMember = (memberStatus) => {
      isMember.value = memberStatus;
      showMemberModal.value = false;
    };

    const goBackToSelection = () => {
      showMemberModal.value = true;
    };

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
    watch(() => booking.value.location, fetchAvailableSlots); // Update when location changes

    const submitBooking = async () => {
      try {
        const formData = new URLSearchParams();
        formData.append("location", booking.value.location);
        formData.append("date", booking.value.date);
        formData.append("time", booking.value.time);
        formData.append("duration", booking.value.duration.toString());

        const response = await axios.post("http://localhost:8000/api/book", formData);

        alert(response.data.message);

        if (!isMember.value) {
          router.push({ path: "/payment", query: {
          location: booking.value.location, // ✅ Pass selected location dynamically
          date: booking.value.date,
          time: booking.value.time,
          duration: booking.value.duration,
        }, });
        } else {
          alert("Booking confirmed! Members do not need payment.");
        }

        setTimeout(fetchAvailableSlots, 500);
      } catch (error) {
        console.error("Booking error:", error);
        alert(error.response?.data?.detail || "An error occurred");
      }
    };

    return {
      booking,
      locations,
      availableTimes,
      fetchAvailableSlots,
      submitBooking,
      showMemberModal,
      selectMember,
      goBackToSelection,
      minDate,
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
input, select {
  @apply text-black bg-white border-gray-300 focus:border-primary focus:ring-primary focus:outline-none;
  padding: 0.5rem;
  border-radius: 0.375rem;
  width: 100%;
}
button {
  @apply py-3 rounded-lg font-bold;
}

/* Member Selection Buttons */
.btn-member {
  @apply bg-green-600 text-white py-3 rounded-lg text-lg font-bold hover:bg-green-700 transition;
}

.btn-non-member {
  @apply bg-blue-600 text-white py-3 rounded-lg text-lg font-bold hover:bg-blue-700 transition;
}

/* Back Button */
.btn-back {
  @apply bg-gray-400 text-white py-3 px-6 rounded-lg text-lg font-bold hover:bg-gray-500 transition;
}

/* Confirm Booking Button */
.btn-confirm {
  @apply bg-green-600 text-white py-3 px-6 rounded-lg text-lg font-bold hover:bg-green-700 transition;
}

/* Modal Styling */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
