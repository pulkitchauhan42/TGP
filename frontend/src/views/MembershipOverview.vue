<template>
  <div class="container mx-auto text-center p-6">
    <h1 class="text-3xl font-bold mb-6">Our Memberships</h1>
    <p class="text-lg mb-6">Choose the perfect membership that suits your needs.</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Individual Membership -->
      <div class="membership-tile">
        <h2 class="text-xl font-semibold mb-2">Individual Membership</h2>
        <p>Perfect for solo golfers looking for unlimited simulator access.</p>
        <router-link to="/memberships/individual" class="btn">View Details</router-link>
      </div>

      <!-- Corporate Membership -->
      <div class="membership-tile">
        <h2 class="text-xl font-semibold mb-2">Corporate Membership</h2>
        <p>Designed for businesses that want to offer golf perks to employees.</p>
        <router-link to="/memberships/corporate" class="btn">View Details</router-link>
      </div>

      <!-- Seasonal Membership -->
      <div class="membership-tile">
        <h2 class="text-xl font-semibold mb-2">Seasonal Membership</h2>
        <p>For those who want flexible golfing options throughout the year.</p>
        <router-link to="/memberships/seasonal" class="btn">View Details</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
}
.membership-tile {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.btn {
  @apply bg-green-600 text-white px-4 py-2 rounded-lg mt-4 inline-block;
}
</style>
