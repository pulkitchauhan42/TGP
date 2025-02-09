<template>
  <div class="container mx-auto p-6">
    <h1 class="text-3xl font-bold text-center mb-6">Book Your Simulator Time</h1>

    <!-- Integrating the Scheduler Component -->
    <TimeScheduler />
  </div>
</template>

<script>
import TimeScheduler from "./TimeScheduler.vue";

export default {
  components: {
    TimeScheduler,
  },
};
</script>
