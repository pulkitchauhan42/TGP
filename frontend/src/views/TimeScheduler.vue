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
          :min="minDate" 
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
import { useRouter } from "vue-router";
import axios from "axios";
import dayjs from "dayjs";

export default {
  setup() {
    const selectedDate = ref(dayjs().format("YYYY-MM-DD"));
    const selectedLocation = ref("Main Facility - 123 Golf Club Ln, Chicago, IL 60601");
    const locations = ref(["Main Facility - 123 Golf Club Ln, Chicago, IL 60601"]);
    const selectedSlots = ref([]);
    const bookedEpochs = ref(new Set());
    const router = useRouter();
    const minDate = computed(() => dayjs().format("YYYY-MM-DD"));
    
    // Get current date and time to block out past slots

    // Format selected date for display
    const selectedDateFormatted = computed(() => dayjs(selectedDate.value).format("dddd, MMMM D, YYYY"));

    // Generate 30-minute slots
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

    // Fetch booked slots
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

    // Clears selection and fetches booked slots when changing date
    const clearSelectionAndFetchBookedSlots = () => {
      selectedSlots.value = [];
      fetchBookedSlots();
    };

    // Date navigation
    const changeDate = (days) => {
      selectedDate.value = dayjs(selectedDate.value).add(days, "day").format("YYYY-MM-DD");
      clearSelectionAndFetchBookedSlots();
    };

    // Slot selection (toggle click)
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

    // Slot styling with disabled/unclickable for past slots
    const slotClass = (slot) => {
      const currentEpoch = Math.floor(Date.now() / 1000);  // Get the current timestamp
      const isPastSlot = slot.epoch < currentEpoch;  // Check if the slot is in the past

      if (bookedEpochs.value.has(slot.epoch) || isPastSlot) {
        return isPastSlot 
          ? "bg-gray-400 text-white cursor-not-allowed line-through"
          : "bg-red-500 text-white cursor-not-allowed"; // Crossed out style for past slots
      }

      return selectedSlots.value.some((s) => s.epoch === slot.epoch)
        ? "bg-green-500 text-white"
        : "bg-gray-200 text-black cursor-pointer";
    };

    // Total duration
    const totalDuration = computed(() => (selectedSlots.value.length * 0.5).toFixed(1));

    // Confirm booking
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

    const userEmail = localStorage.getItem("userEmail"); // Make sure the email is stored in localStorage
    const amountToPay = 50 * (selectedSlots.value.length * 0.5); // Calculate the total amount in dollars
    const amountToPayInCents = amountToPay * 100; // convert to cents
    const requestData = new URLSearchParams();
    requestData.append("location", selectedLocation.value);
    requestData.append("date", selectedDate.value);
    requestData.append("time", selectedSlots.value[0].label);
    requestData.append("duration", (selectedSlots.value.length * 0.5).toString());
    requestData.append("email", userEmail); // Ensure we pass the email here

    const response = await axios.post(
      "http://localhost:8000/api/book",
      requestData,
      { headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/x-www-form-urlencoded" } }
    );

    if (response.data.redirect_to_payment) {
      // Check if the user needs to be redirected to Stripe
      const amount = response.data.amount_to_pay || amountToPay; // fallback to the calculated amount
      const availableHours = response.data.available_hours;

      // Redirect to the appropriate payment page
      router.push({
        path: response.data.stripe_session_url, // Should be '/payment/member-payment' or '/payment/non-member-payment'
        query: {
          location: selectedLocation.value,
          date: selectedDate.value,
          time: selectedSlots.value[0].label,
          duration: (selectedSlots.value.length * 0.5).toString(),
          amount: amount,  // Pass the correct amount
          availableHours: availableHours, // Pass available hours for member users
        },
      });
      console.log('Amount to Pay (in cents): ', amountToPayInCents);

    } else {
      alert("✅ Booking confirmed! No payment required.");
    }
  } catch (error) {
    console.error("❌ Booking error:", error);
    alert(error.response?.data?.detail || "An error occurred while booking.");
  }
};




    return { 
      selectedDate, 
      selectedDateFormatted, 
      changeDate, 
      selectedLocation, 
      locations, 
      morningSlots, 
      afternoonSlots, 
      nightSlots, 
      selectedSlots, 
      bookedEpochs, 
      toggleSlot, 
      slotClass, 
      confirmBooking, 
      totalDuration, 
      clearSelectionAndFetchBookedSlots ,
      minDate
    };
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
