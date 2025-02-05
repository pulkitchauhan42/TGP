<template>
  <div class="container mx-auto py-12 px-6 max-w-3xl">
    <h1 class="text-4xl font-serif font-bold text-primary mb-6 text-center">Contact Us</h1>

    <!-- Contact Info -->
    <div class="text-center mb-10">
      <p class="text-lg text-textDark">📞 Call us: <a href="tel:6304186267" class="text-secondary font-bold">630-418-6267</a></p>
      <p class="text-lg text-textDark">📧 Email us: <a href="mailto:bookings@thatgolfplace.com" class="text-secondary font-bold">bookings@thatgolfplace.com</a></p>
    </div>

    <!-- Contact Form -->
    <form @submit.prevent="submitForm" class="bg-white shadow-lg rounded-lg p-6">
      <div class="mb-4">
        <label class="block text-sm font-semibold text-textDark mb-1">Full Name</label>
        <input v-model="form.name" type="text" required class="w-full border border-gray-300 rounded-md p-2">
      </div>

      <div class="mb-4">
        <label class="block text-sm font-semibold text-textDark mb-1">Email Address</label>
        <input v-model="form.email" type="email" required class="w-full border border-gray-300 rounded-md p-2">
      </div>

      <div class="mb-4">
        <label class="block text-sm font-semibold text-textDark mb-1">Message</label>
        <textarea v-model="form.message" required rows="4" class="w-full border border-gray-300 rounded-md p-2"></textarea>
      </div>

      <button type="submit" class="w-full bg-primary text-textLight py-2 rounded-md font-bold hover:bg-green-700 transition">
        Send Message
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      form: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        await axios.post("http://localhost:8000/api/contact", new FormData(document.querySelector("form")));
        this.$router.push("/contact-confirmation"); // Redirect to confirmation page
      } catch (error) {
        alert("Something went wrong. Please try again.");
      }
    },
  },
};
</script>
