<template>
    <div class="payment-container">
      <h2 class="text-2xl font-semibold">Member Payment</h2>
      <p>
        You have selected {{ duration }} hour(s) for booking, but you only have {{ availableHours }} hour(s) in your account.
      </p>
      <p>
        You need to pay for the additional <strong>{{ extraHours }} hour(s)</strong>.
      </p>
      <p>
        Amount to pay: <strong>${{ amountToPay }}</strong>
      </p>
      <button @click="redirectToStripe" class="bg-green-600 text-white px-4 py-2 rounded-lg">
        Continue to Payment
      </button>
    </div>
  </template>
  
  <script>
  import { useRouter } from "vue-router";
  import axios from "axios";
  
  export default {
    setup() {
      const router = useRouter();
      const query = router.currentRoute.value.query;
  
      const availableHours = parseFloat(query.availableHours);
      const duration = parseFloat(query.duration);
      const extraHours = duration > availableHours ? duration - availableHours : 0;
      const amountToPay = extraHours * 50; // Assuming $50 per hour
      const location = query.location;
      const date = query.date;
      const time = query.time;
      const userEmail = localStorage.getItem("userEmail");
      
      // Make sure it's not NaN or negative
      if (isNaN(extraHours) || extraHours <= 0) {
          extraHours == 0; // Set to 0 if the calculation is wrong
      }
      
      const redirectToStripe = async () => {
        try {
          const response = await axios.post("http://localhost:8000/api/create-checkout-session", {
            location: location,
            date: date,
            time: time,
            duration: duration,
            amount: (amountToPay * 100),
            email: userEmail,
          });
          window.location.href = response.data.checkout_url;
        } catch (error) {
          console.error("❌ Error redirecting to Stripe:", error);
          alert("An error occurred while processing your payment.");
        }
      };
  
      return {
        availableHours,
        duration,
        extraHours,
        amountToPay,
        redirectToStripe,
      };
    },
  };
  </script>
  

<style scoped>
.container {
  max-width: 600px;
}

.btn-confirm {
  @apply w-full bg-green-600 text-white py-2 rounded-lg font-bold hover:bg-green-700 transition;
}

/* Disabled Button Styling */
.btn-confirm:disabled {
  @apply bg-gray-400 cursor-not-allowed;
}

label {
  @apply text-gray-800 font-medium;
}
</style>
