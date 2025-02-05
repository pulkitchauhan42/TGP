import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import AboutPage from '@/views/AboutPage.vue';
import BookingPage from '@/views/BookingPage.vue';
import ContactPage from '@/views/ContactPage.vue';
//import ContactConfirmation from '@/views/ContactConfirmation.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: AboutPage },
  { path: '/booking', component: BookingPage },
  { path: '/contact', component: ContactPage },
  //{ path: '/contact-confirmation', component: ContactConfirmation },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
