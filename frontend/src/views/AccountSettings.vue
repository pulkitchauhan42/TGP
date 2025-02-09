<template>
  <div class="container mx-auto p-6 max-w-lg">
    <h1 class="text-3xl font-bold text-center mb-6 text-black">Account Settings</h1>

    <!-- ✅ Update Profile Form -->
    <form @submit.prevent="updateProfile" class="bg-white p-6 shadow-lg rounded-lg">
      <div class="mb-4">
        <label class="block text-lg font-semibold text-gray-700">Full Name:</label>
        <input type="text" v-model="user.full_name" class="input-field" />
      </div>

      <div class="mb-4">
        <label class="block text-lg font-semibold text-gray-700">Email:</label>
        <input type="email" v-model="user.email" class="input-field bg-gray-200" disabled />
      </div>

      <div class="mb-4">
        <label class="block text-lg font-semibold text-gray-700">New Password:</label>
        <input type="password" v-model="newPassword" class="input-field" placeholder="Enter new password" />
      </div>

      <button type="submit" class="btn-primary w-full">Update Profile</button>
      <p v-if="successMessage" class="text-green-600 mt-2 text-center">{{ successMessage }}</p>
      <p v-if="errorMessage" class="text-red-600 mt-2 text-center">{{ errorMessage }}</p>
    </form>

    <!-- ✅ Membership Info -->
    <div v-if="user.is_member" class="mt-6 bg-green-100 p-4 rounded-lg">
      <h2 class="text-xl font-bold text-green-800">Membership Status: Active</h2>
      <p class="text-lg text-green-700">Remaining Hours: <strong>{{ user.member_hours }}</strong></p>
    </div>

    <!-- ✅ Past Bookings -->
    <div class="mt-6">
      <h2 class="text-xl font-bold text-gray-800">Past Bookings</h2>
      <ul v-if="bookings.length > 0" class="mt-2 bg-white p-4 rounded-lg shadow-md">
        <li v-for="booking in bookings" :key="booking.date + booking.time" class="bg-gray-100 p-3 mb-2 rounded-lg text-black">
          <p><strong>Date:</strong> {{ booking.date }}</p>
          <p><strong>Time:</strong> {{ booking.time }}</p>
          <p><strong>Duration:</strong> {{ booking.duration }} hrs</p>
          <p><strong>Location:</strong> {{ booking.location }}</p>
        </li>
      </ul>
      <p v-else class="text-gray-700 mt-2">No past bookings found.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup(_, { emit }) { // ✅ Accept `emit` to send events
    const user = ref({ full_name: "", email: "", is_member: false, member_hours: 0 });
    const bookings = ref([]);
    const newPassword = ref("");
    const successMessage = ref("");
    const errorMessage = ref("");

    // ✅ Fetch user data
    const fetchUserData = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) return;

      try {
        const response = await axios.get("http://localhost:8000/api/me", {
          headers: { Authorization: `Bearer ${token}` },
        });
        user.value = response.data;
      } catch (error) {
        console.error("❌ Error fetching user data:", error);
      }
    };

    // ✅ Fetch user bookings
    const fetchUserBookings = async () => {
      const token = localStorage.getItem("authToken");
      if (!token) return;

      try {
        const response = await axios.get("http://localhost:8000/api/my-bookings", {
          headers: { Authorization: `Bearer ${token}` },
        });
        bookings.value = response.data.bookings;
      } catch (error) {
        console.error("❌ Error fetching bookings:", error);
      }
    };

    // ✅ Update user profile
    const updateProfile = async () => {
      successMessage.value = "";
      errorMessage.value = "";

      const token = localStorage.getItem("authToken");
      if (!token) {
        errorMessage.value = "You must be logged in to update your profile.";
        return;
      }

      try {
        const requestData = new URLSearchParams();
        requestData.append("full_name", user.value.full_name);
        if (newPassword.value) {
          requestData.append("new_password", newPassword.value);
        }

        const response = await axios.put("http://localhost:8000/api/update-user", requestData, {
          headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/x-www-form-urlencoded" },
        });

        successMessage.value = response.data.message;
        newPassword.value = ""; // Clear password field after update

        // ✅ Emit event to update the header
        emit("profileUpdated");

      } catch (error) {
        console.error("❌ Error updating profile:", error);
        errorMessage.value = "Failed to update profile. Please try again.";
      }
    };

    onMounted(() => {
      fetchUserData();
      fetchUserBookings();
    });

    return { user, bookings, newPassword, updateProfile, successMessage, errorMessage };
  },
};
</script>


<style scoped>
.container {
  max-width: 600px;
}

.input-field {
  @apply border border-gray-400 p-2 rounded w-full mt-2 text-gray-900;
}

.btn-primary {
  @apply bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition;
}
</style>
