<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center text-gray-900 mb-6">Contact Us</h1>

    <form @submit.prevent="submitContactForm" class="max-w-lg mx-auto bg-white p-6 shadow-lg rounded-lg border border-gray-300">
      <h2 class="text-xl font-semibold mb-4 text-gray-800">Send us a message</h2>

      <label for="name" class="block text-gray-700 font-semibold">Name:</label>
      <input type="text" id="name" v-model="contact.name" class="input-field" required />

      <label for="email" class="block text-gray-700 font-semibold mt-4">Email:</label>
      <input type="email" id="email" v-model="contact.email" class="input-field" required />

      <label for="message" class="block text-gray-700 font-semibold mt-4">Message:</label>
      <textarea id="message" v-model="contact.message" rows="4" class="input-field" required></textarea>

      <button type="submit" class="btn-submit mt-4">Send Message</button>
    </form>

    <p v-if="successMessage" class="text-green-600 text-center font-semibold mt-4">{{ successMessage }}</p>
    <p v-if="errorMessage" class="text-red-600 text-center font-semibold mt-4">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";

export default {
  setup() {
    const contact = ref({
      name: "",
      email: "",
      message: "",
    });

    const successMessage = ref("");
    const errorMessage = ref("");

    const submitContactForm = async () => {
      successMessage.value = "";
      errorMessage.value = "";

      try {
        const response = await axios.post("http://localhost:8000/api/contact", new URLSearchParams({
          name: contact.value.name,
          email: contact.value.email,
          message: contact.value.message,
        }));

        successMessage.value = response.data.message;
        contact.value = { name: "", email: "", message: "" }; // Reset form after successful submission
      } catch (error) {
        console.error("❌ Contact form error:", error);
        errorMessage.value = "Failed to send message. Please try again.";
      }
    };

    return {
      contact,
      submitContactForm,
      successMessage,
      errorMessage,
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

.btn-submit {
  @apply w-full bg-blue-600 text-white py-2 rounded-lg font-bold hover:bg-blue-700 transition;
}
</style>
