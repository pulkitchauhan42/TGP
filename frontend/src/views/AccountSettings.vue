<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center text-gray-900 mb-6">Account Settings</h1>

    <div class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Profile Information</h2>
      
      <div class="mb-4">
        <label class="block text-lg font-semibold text-gray-700 mb-1">Email:</label>
        <input type="email" v-model="user.email" disabled class="input-field" />
      </div>

      <div class="mb-4">
        <label class="block text-lg font-semibold text-gray-700 mb-1">Change Password:</label>
        <input type="password" v-model="newPassword" placeholder="New Password" class="input-field" />
      </div>

      <button @click="updatePassword" class="btn-save">Update Password</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const user = ref({ email: "" });
    const newPassword = ref("");

    onMounted(() => {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        user.value = JSON.parse(storedUser);
      }
    });

    const updatePassword = () => {
      if (!newPassword.value) {
        alert("Please enter a new password.");
        return;
      }
      alert("Password updated successfully!");
      newPassword.value = "";
    };

    return { user, newPassword, updatePassword };
  }
};
</script>
