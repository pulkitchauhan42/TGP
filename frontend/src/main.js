import './main.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Import the router

window.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false;

const app = createApp(App);
app.use(router); // Register the router
app.mount('#app');
