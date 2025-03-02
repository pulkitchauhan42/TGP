import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../views/HomePage.vue";
import AboutPage from "../views/AboutPage.vue";
import BookingPage from "../views/BookingPage.vue";
import ContactPage from "../views/ContactPage.vue";
import MembershipOverview from "../views/MembershipOverview.vue";
import IndividualMemberships from "../views/IndividualMemberships.vue";
import CorporateMemberships from "../views/CorporateMemberships.vue";
import SeasonalMemberships from "../views/SeasonalMemberships.vue";
import PaymentPage from "../views/PaymentPage.vue";
import PaymentSuccess from "../views/PaymentSuccess.vue";
import LoginPage from "../views/LoginSignup.vue";
import SignupPage from "../views/SignupPage.vue";
import ManageBookings from "../views/ManageBookings.vue"; // ✅ Newly added
import AccountSettings from "../views/AccountSettings.vue"; // ✅ Newly added
import PaymentConfirmation from "../views/PaymentConfirmation.vue"
import MemberPaymentPage from "../views/MemberPaymentPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/login", component: LoginPage },
  { path: "/about", component: AboutPage },
  { path: "/booking", component: BookingPage },
  { path: "/contact", component: ContactPage },
  { path: "/memberships", component: MembershipOverview },
  { path: "/memberships/individual", component: IndividualMemberships },
  { path: "/memberships/corporate", component: CorporateMemberships },
  { path: "/memberships/seasonal", component: SeasonalMemberships },
  { path: "/payment/non-member-payment", component: PaymentPage, meta: { requiresAuth: true } },
  { path: "/payment-success", component: PaymentSuccess },
  { path: "/signup", component: SignupPage },
  { path: "/manage-bookings", component: ManageBookings, meta: { requiresAuth: true } }, // ✅ Protected Route
  { path: "/account-settings", component: AccountSettings, meta: { requiresAuth: true } }, // ✅ Protected Route
  { path: "/payment-confirmation", component: PaymentConfirmation, meta: { requiresAuth: true } }, // ✅ Protected Route
  { path: "/payment/member-payment", component: MemberPaymentPage, meta: { requiresAuth: true } }, // ✅ Protected Route
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Route Guard: Only require login for protected pages (like payment)
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem("authToken");

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ path: "/login", query: { redirect: to.fullPath } });
  } else {
    next();
  }
});

export default router;
