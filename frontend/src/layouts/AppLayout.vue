<template>
  <div>
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/about">About</router-link>
        <router-link to="/booking">Booking</router-link>
        <router-link to="/contact">Contact</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
    <footer>
      <p>&copy; 2025 That Golf Place</p>
    </footer>
  </div>
</template>

<style>
header {
  background: #333;
  padding: 1rem;
  text-align: center;
}
nav a {
  color: white;
  margin: 0 15px;
  text-decoration: none;
}
footer {
  margin-top: 20px;
  text-align: center;
  padding: 1rem;
  background: #222;
  color: white;
}
</style>
