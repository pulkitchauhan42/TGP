<template>
  <div class="scheduler-container border border-gray-300 p-6 rounded-lg shadow-md bg-white">
    <!-- 📅 Date & Location Selection -->
    <div class="flex justify-between items-center mb-4">
      <button @click="changeDate(-1)" class="text-lg px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">←</button>

      <div class="text-center">
        <label for="date" class="block text-lg font-semibold text-black">Select Date:</label>
        <input 
          type="date" 
          id="date"
          v-model="selectedDate" 
          @change="clearSelectionAndFetchBookedSlots" 
          class="border border-gray-300 p-2 rounded text-black cursor-pointer"
        />
      </div>

      <button @click="changeDate(1)" class="text-lg px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">→</button>
    </div>

    <div class="text-center mb-4">
      <label for="location" class="block text-lg font-semibold text-black">Select Location:</label>
      <select v-model="selectedLocation" id="location" @change="clearSelectionAndFetchBookedSlots" class="border p-2 rounded bg-white text-black">
        <option v-for="location in locations" :key="location" :value="location">{{ location }}</option>
      </select>
    </div>

    <!-- 🕒 Time Slot Selection -->
    <h2 class="text-xl font-bold text-center mb-4 text-black">{{ selectedDateFormatted }}</h2>
    
    <div class="grid grid-cols-3 gap-4">
      <!-- Morning Column -->
      <div>
        <h3 class="text-lg font-bold text-center mb-2 text-gray-900 bg-gray-200 p-2 rounded">Morning</h3>
        <div v-for="slot in morningSlots" :key="slot.epoch" :class="slotClass(slot)" @click="toggleSlot(slot)">
          {{ slot.label }}
        </div>
      </div>

      <!-- Afternoon Column -->
      <div>
        <h3 class="text-lg font-bold text-center mb-2 text-gray-900 bg-gray-200 p-2 rounded">Afternoon</h3>
        <div v-for="slot in afternoonSlots" :key="slot.epoch" :class="slotClass(slot)" @click="toggleSlot(slot)">
          {{ slot.label }}
        </div>
      </div>

      <!-- Night Column -->
      <div>
        <h3 class="text-lg font-bold text-center mb-2 text-gray-900 bg-gray-200 p-2 rounded">Night</h3>
        <div v-for="slot in nightSlots" :key="slot.epoch" :class="slotClass(slot)" @click="toggleSlot(slot)">
          {{ slot.label }}
        </div>
      </div>
    </div>

    <!-- Total Duration & Confirm Button -->
    <div class="mt-6 text-center">
      <p class="text-lg font-semibold mb-2 text-black">
        Selected Time: <span class="text-green-600">{{ totalDuration }} hours</span>
      </p>
      <button 
        @click="confirmBooking"
        class="bg-green-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        :disabled="selectedSlots.length === 0"
      >
        Confirm Booking
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import dayjs from "dayjs";

export default {
  setup() {
    const selectedDate = ref(dayjs().format("YYYY-MM-DD"));
    const selectedLocation = ref("Main Facility - 123 Golf Club Ln, Chicago, IL 60601");
    const locations = ref(["Main Facility - 123 Golf Club Ln, Chicago, IL 60601"]);
    const selectedSlots = ref([]);
    const bookedEpochs = ref(new Set());

    // ✅ Format Selected Date for Display
    const selectedDateFormatted = computed(() => dayjs(selectedDate.value).format("dddd, MMMM D, YYYY"));

    // ✅ Generate 30-Minute Slots
    const generateSlots = (startHour, endHour) => {
      const slots = [];
      for (let hour = startHour; hour <= endHour; hour++) {
        for (let minute of ["00", "30"]) {
          const slotTime = dayjs(`${selectedDate.value} ${hour}:${minute}`, "YYYY-MM-DD H:mm");
          slots.push({
            label: slotTime.format("h:mm A"),
            epoch: slotTime.unix(),
          });
        }
      }
      return slots;
    };

    const morningSlots = computed(() => generateSlots(4, 11));
    const afternoonSlots = computed(() => generateSlots(12, 18));
    const nightSlots = computed(() => [...generateSlots(19, 23), ...generateSlots(0, 3)]);

    // ✅ Fetch Booked Slots
    const fetchBookedSlots = async () => {
      bookedEpochs.value.clear();
      try {
        const response = await axios.get("http://localhost:8000/api/booked-slots", {
          params: { date: selectedDate.value, location: selectedLocation.value },
        });

        if (response.data.bookedSlots) {
          response.data.bookedSlots.forEach((epochTime) => {
            bookedEpochs.value.add(Number(epochTime));
          });
        }
      } catch (error) {
        console.error("❌ Error fetching booked slots:", error);
      }
    };

    onMounted(fetchBookedSlots);
    watch(selectedDate, fetchBookedSlots);

    // ✅ Clears Selection & Fetches Slots When Changing Date
    const clearSelectionAndFetchBookedSlots = () => {
      selectedSlots.value = [];
      fetchBookedSlots();
    };

    // ✅ Date Navigation
    const changeDate = (days) => {
      selectedDate.value = dayjs(selectedDate.value).add(days, "day").format("YYYY-MM-DD");
      clearSelectionAndFetchBookedSlots();
    };

    // ✅ Slot Selection (Toggle Click)
    const toggleSlot = (slot) => {
      if (bookedEpochs.value.has(slot.epoch)) return;

      const index = selectedSlots.value.findIndex((s) => s.epoch === slot.epoch);
      if (index !== -1) {
        selectedSlots.value.splice(index, 1); // Unselect slot if already selected
        return;
      }

      if (selectedSlots.value.length > 0) {
        const lastSelected = selectedSlots.value[selectedSlots.value.length - 1];
        if (Math.abs(slot.epoch - lastSelected.epoch) !== 1800) {
          alert("You must select consecutive time slots.");
          return;
        }
      }

      if (selectedSlots.value.length < 8) {
        selectedSlots.value.push(slot);
      } else {
        alert("You can only book up to 4 hours!");
      }
    };

    // ✅ Slot Styling
    const slotClass = (slot) => {
      return bookedEpochs.value.has(slot.epoch)
        ? "bg-red-500 text-white cursor-not-allowed"
        : selectedSlots.value.some((s) => s.epoch === slot.epoch)
        ? "bg-green-500 text-white"
        : "bg-gray-200 text-black cursor-pointer";
    };

    // ✅ Total Duration
    const totalDuration = computed(() => (selectedSlots.value.length * 0.5).toFixed(1));

    // ✅ Confirm Booking
    const confirmBooking = async () => {
      if (selectedSlots.value.length === 0) {
        alert("Please select at least one slot.");
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        if (!token) {
          alert("You are not logged in. Please sign in to book.");
          return;
        }

        const requestData = new URLSearchParams();
        requestData.append("location", selectedLocation.value);
        requestData.append("date", selectedDate.value);
        requestData.append("time", selectedSlots.value[0].label);
        requestData.append("duration", (selectedSlots.value.length * 0.5).toString());

        const response = await axios.post(
          "http://localhost:8000/api/book",
          requestData,
          { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/x-www-form-urlencoded" } }
        );

        alert(response.data.message);
        selectedSlots.value = [];
        fetchBookedSlots();
      } catch (error) {
        console.error("❌ Booking error:", error);
        alert(error.response?.data?.detail || "An error occurred while booking.");
      }
    };

    return { selectedDate, selectedDateFormatted, changeDate, selectedLocation, locations, morningSlots, afternoonSlots, nightSlots, selectedSlots, bookedEpochs, toggleSlot, slotClass, confirmBooking, totalDuration, clearSelectionAndFetchBookedSlots };
  },
};
</script>





<style scoped>
.scheduler-container {
  max-width: 900px;
  margin: auto;
}

.grid div > div {
  @apply p-2 rounded-md text-center m-1 transition cursor-pointer;
}
</style>
