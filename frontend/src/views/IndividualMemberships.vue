<template>
  <div class="container mx-auto text-center p-6">
    <h1 class="text-3xl font-bold mb-6">Individual Membership</h1>
    <p class="text-lg">Enjoy unlimited access to our golf simulators with this membership.</p>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
      <div class="tier-card">
        <h2 class="text-xl font-semibold mb-2">Silver Tier</h2>
        <p>Basic simulator access for individuals.</p>
      </div>

      <div class="tier-card">
        <h2 class="text-xl font-semibold mb-2">Gold Tier</h2>
        <p>Enhanced perks with exclusive time slots.</p>
      </div>

      <div class="tier-card">
        <h2 class="text-xl font-semibold mb-2">Platinum Tier</h2>
        <p>VIP experience with unlimited access.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
}
.tier-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
