<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Manage Your Bookings</h1>

    <!-- User Info -->
    <div class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300">
      <p class="text-lg font-semibold text-gray-800"><strong>Email:</strong> {{ user.email }}</p>

      <p v-if="user.is_member" class="text-lg font-semibold text-green-600">
        <strong>Remaining Hours:</strong> {{ user.member_hours }} hours
      </p>
      <p v-else class="text-lg font-semibold text-red-600">
        You are not a member.
        <router-link to="/memberships" class="text-blue-600 hover:underline">Join here</router-link>.
      </p>
    </div>

    <!-- User Bookings -->
    <h2 class="text-2xl font-semibold text-center mt-8">Your Bookings</h2>

    <div v-if="bookings.length > 0" class="mt-4 space-y-4">
      <div
        v-for="booking in sortedBookings"
        :key="booking.date + booking.time"
        class="bg-white p-4 rounded-lg shadow border border-gray-300"
      >
        <p class="text-gray-800"><strong>Location:</strong> {{ booking.location }}</p>
        <p class="text-gray-800"><strong>Date:</strong> {{ booking.date }}</p>
        <p class="text-gray-800"><strong>Time:</strong> {{ booking.time }}</p>
        <p class="text-gray-800"><strong>Duration:</strong> {{ booking.duration }} hour(s)</p>

        <!-- Cancel Button (Only if More than 12 Hours Before Booking) -->
        <button
          v-if="canCancel(booking.date, booking.time)"
          @click="cancelBooking(booking)"
          class="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Cancel Booking
        </button>
      </div>
    </div>

    <p v-else class="text-center text-gray-600 mt-4">You have no bookings yet.</p>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import dayjs from "dayjs";

export default {
  setup() {
    const user = ref({ email: "", is_member: false, member_hours: 0 });
    const bookings = ref([]);

    // Fetch user details
    const fetchUserData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/me", {
          headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
        });
        user.value = response.data;
      } catch (error) {
        console.error("❌ Error fetching user data:", error);
      }
    };

    // Fetch user bookings
    const fetchUserBookings = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/my-bookings", {
          headers: { Authorization: `Bearer ${localStorage.getItem("authToken")}` },
        });
        bookings.value = response.data.bookings || [];
      } catch (error) {
        console.error("❌ Error fetching user bookings:", error);
      }
    };

    // Computed property to sort bookings chronologically
    const sortedBookings = computed(() => {
      return bookings.value.slice().sort((a, b) => {
        return (
          dayjs(`${a.date} ${a.time}`, "YYYY-MM-DD h:mm A").valueOf() -
          dayjs(`${b.date} ${b.time}`, "YYYY-MM-DD h:mm A").valueOf()
        );
      });
    });

    // Check if booking can be canceled (more than 12 hours away)
    const canCancel = (date, time) => {
      const bookingDateTime = dayjs(`${date} ${time}`, "YYYY-MM-DD h:mm A");
      return bookingDateTime.diff(dayjs(), "hours") > 24;
    };

    // Cancel Booking
    const cancelBooking = async (booking) => {
  if (!confirm("Are you sure you want to cancel this booking?")) return;

  try {
    // Send DELETE request to backend
    const response = await axios.delete(`http://localhost:8000/api/cancel-booking/${booking.location}/${booking.date}/${booking.time}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("authToken")}`,
      },
    });

    // Show success message
    alert(response.data.message);

    // Remove canceled booking from the bookings list (directly update the frontend state)
    const index = bookings.value.findIndex(
      (b) => b.date === booking.date && b.time === booking.time && b.location === booking.location
    );
    
    if (index !== -1) {
      bookings.value.splice(index, 1);  // Remove the canceled booking from the list
    }

    // Optionally, re-fetch user data and bookings (if you want to ensure data is synchronized with the backend)
    fetchUserData(); // Refresh user data to reflect changes (e.g., updated hours for members)
    fetchUserBookings(); // Refresh bookings list after cancellation

  } catch (error) {
    console.error("❌ Error canceling booking:", error);
    alert(error.response?.data?.detail || "Could not cancel booking.");
  }
};


    onMounted(() => {
      fetchUserData();
      fetchUserBookings();
    });

    return { user, bookings, sortedBookings, cancelBooking, canCancel };
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
