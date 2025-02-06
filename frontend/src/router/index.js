import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import AboutPage from "../views/AboutPage.vue";
import BookingPage from "../views/BookingPage.vue";
import ContactPage from "../views/ContactPage.vue";
import MembershipOverview from "../views/MembershipOverview.vue";
import IndividualMemberships from "../views/IndividualMemberships.vue";
import CorporateMemberships from "../views/CorporateMemberships.vue";
import SeasonalMemberships from "../views/SeasonalMemberships.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/about", component: AboutPage },
  { path: "/booking", component: BookingPage },
  { path: "/contact", component: ContactPage },
  { path: "/memberships", component: MembershipOverview },
  { path: "/memberships/individual", component: IndividualMemberships },
  { path: "/memberships/corporate", component: CorporateMemberships },
  { path: "/memberships/seasonal", component: SeasonalMemberships },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
