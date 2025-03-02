<template>
  <div>
    <h2 class="text-2xl font-semibold">Non-Member Payment</h2>

    <!-- Show message when extra hours are required -->
    <p v-if="amount > 0">
      You have selected <strong>{{ duration }} hour(s)</strong> for booking. As a non-member, you need to pay the full amount to complete your booking.
    </p>

    <!-- Show the amount to pay -->
    <p v-if="amount > 0">Amount to pay: <strong>${{ amount / 100 }}</strong></p>

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
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const router = useRouter();
    const query = router.currentRoute.value.query;

    // Access the data passed in the query params
    const amount = parseFloat(query.amount);  // Amount to pay
    const duration = parseFloat(query.duration);  // Duration of the booking
    const location = query.location;
    const date = query.date;
    const time = query.time;
    const userEmail = localStorage.getItem("userEmail");

    


    // Get the email from localStorage (assuming user is logged in)
    const email = localStorage.getItem("userEmail");

    // Validate the email
    if (!email || typeof email !== "string") {
      console.error("❌ Invalid email");
      alert("You are not logged in. Please log in again.");
      router.push("/login");  // Redirect to login page
      return;
    }

    console.log("Email fetched from localStorage:", email);  // Debugging

    // Redirect to Stripe checkout with correct amount
    const redirectToStripe = async () => {
      try {
        // Convert the amount to cents before sending to the backend
        const amountInCents = amount ;
        
        console.log("Redirecting to Stripe with amount:", amountInCents); // Debugging
        const response = await axios.post("http://localhost:8000/api/create-checkout-session", {
          location,
          date,
          time,
          duration,
          amount: amountInCents,  // Pass the correct amount in cents to the backend
          email: userEmail,  // Pass the email to the backend
        });

        // Redirect the user to Stripe checkout
        window.location.href = response.data.checkout_url;
      } catch (error) {
        console.error("❌ Error redirecting to Stripe:", error);
        alert("An error occurred while processing your payment.");
      }
    };

    // Cancel the booking and go back to the booking page
    const cancelBooking = () => {
      router.push("/booking");
    };

    return {
      amount,
      duration,
      location,
      date,
      time,
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
