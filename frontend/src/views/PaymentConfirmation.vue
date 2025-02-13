<template>
    <div>
      <h2 class="text-2xl font-semibold">Payment Confirmation</h2>
  
      <!-- Show message when extra hours are required -->
      <p v-if="extraHours > 0">
        You have selected <strong>{{ duration }} hour(s)</strong>, but you only have
        <strong>{{ availableHours }} hour(s)</strong> left in your account.
        You need to pay for the additional <strong>{{ extraHours }}</strong> hour(s).
      </p>
  
      <!-- Show message when no extra hours are required -->
      <p v-else>
        You have enough hours to book this session without additional payment.
      </p>
  
      <!-- Show the amount to pay if extra hours are needed -->
      <p v-if="extraHours > 0">Amount to pay: <strong>${{ amountToPay }}</strong></p>
  
      <!-- Buttons for user actions -->
      <button @click="redirectToStripe" class="mt-4 px-4 py-2 bg-green-600 text-white rounded">
        Continue to Payment
      </button>
  
      <button @click="cancelBooking" class="mt-4 ml-2 px-4 py-2 bg-gray-400 text-white rounded">
        Cancel Booking
      </button>
    </div>
  </template>
  
  <script>
  import { computed } from "vue";
  import { useRouter } from "vue-router";
  
  export default {
    setup() {
      const router = useRouter();
      const query = router.currentRoute.value.query;
  
      // Access the data passed in the query params
      const availableHours = parseFloat(query.availableHours);
      const duration = parseFloat(query.duration);
      //const amount = parseFloat(query.amount);
      const checkoutUrl = query.checkout_url; // Get the Stripe checkout URL
  
      // Calculate extra hours that need to be paid for
      const extraHours = computed(() => {
        const extra = duration > availableHours ? duration - availableHours : 0;
        return extra;
      });
  
      const amountToPay = computed(() => {
        return extraHours.value * 50; // Assuming $50 per hour
      });
  
      // Redirect to Stripe checkout with correct amount
      const redirectToStripe = () => {
        if (checkoutUrl) {
          window.location.href = checkoutUrl; // Redirect to the Stripe session URL
        }
      };
  
      // Cancel the booking and go back to the booking page
      const cancelBooking = () => {
        router.push("/booking");
      };
  
      return {
        extraHours,
        amountToPay,
        availableHours,
        duration,
        redirectToStripe,
        cancelBooking,
      };
    },
  };
  </script>
  
  <style scoped>
  .confirmation-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    text-align: center;
  }
  </style>
  