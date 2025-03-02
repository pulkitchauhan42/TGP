import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Import the router
import './main.css';

// Import FontAwesome core library
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons'; // Import solid icons

// Add icons to the library
library.add(fas);

const app = createApp(App);

// Register FontAwesomeIcon component globally
app.component('font-awesome-icon', FontAwesomeIcon);

app.use(router); // Register the router
app.mount('#app');
