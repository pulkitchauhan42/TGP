import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import Stripe from "stripe";

export default {
  async fetch(request, env) {
    let url = new URL(request.url);
    let method = request.method;

    // ✅ Load Secrets from Environment Variables
    const SECRET_KEY = env.JWT_SECRET;
    const stripe = new Stripe(env.STRIPE_SECRET_KEY);

    try {
      // ✅ User Signup (Persists User in Cloudflare D1)
      if (method === "POST" && url.pathname === "/api/signup") {
        const { email, password, full_name, is_member, member_hours } = await request.json();

        let existingUser = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(email).first();
        if (existingUser) {
          return new Response(JSON.stringify({ error: "User already exists" }), { status: 400 });
        }

        const hashedPassword = await bcrypt.hash(password, 10);
        await env.DB.prepare(
          "INSERT INTO users (email, full_name, password, is_member, member_hours) VALUES (?, ?, ?, ?, ?)"
        ).bind(email, full_name, hashedPassword, is_member, member_hours).run();

        const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: "1h" });

        return new Response(JSON.stringify({ message: "User registered!", token, is_member }), {
          headers: { "Content-Type": "application/json" }
        });
      }

      // ✅ User Login (Verifies from Cloudflare D1)
      if (method === "POST" && url.pathname === "/api/login") {
        const { email, password } = await request.json();

        let user = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(email).first();
        if (!user || !(await bcrypt.compare(password, user.password))) {
          return new Response(JSON.stringify({ error: "Invalid credentials" }), { status: 400 });
        }

        const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: "1h" });

        return new Response(JSON.stringify({ access_token: token, token_type: "bearer", is_member: user.is_member }), {
          headers: { "Content-Type": "application/json" }
        });
      }

      // ✅ Authentication Middleware
      let authHeader = request.headers.get("Authorization");
      let currentUser = null;
      if (authHeader && authHeader.startsWith("Bearer ")) {
        try {
          const token = authHeader.split(" ")[1];
          const payload = jwt.verify(token, SECRET_KEY);
          currentUser = await env.DB.prepare("SELECT * FROM users WHERE email = ?").bind(payload.sub).first();
          if (!currentUser) throw new Error();
        } catch (err) {
          return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
        }
      }

      // ✅ Get Booked Slots from Cloudflare D1
      if (method === "GET" && url.pathname === "/api/booked-slots") {
        const date = url.searchParams.get("date");
        const location = url.searchParams.get("location") || "That Golf Place - Main Location";

        let bookings = await env.DB.prepare("SELECT * FROM bookings WHERE date = ? AND location = ?")
          .bind(date, location).all();

        return new Response(JSON.stringify({ bookedSlots: bookings.results }), {
          headers: { "Content-Type": "application/json" }
        });
      }

      // ✅ Book a Slot
      if (method === "POST" && url.pathname === "/api/book") {
        if (!currentUser) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });

        const { date, time, duration, location } = await request.json();
        await env.DB.prepare(
          "INSERT INTO bookings (email, date, time, duration, location) VALUES (?, ?, ?, ?, ?)"
        ).bind(currentUser.email, date, time, duration, location).run();

        return new Response(JSON.stringify({ message: "Booking successful!" }), {
          headers: { "Content-Type": "application/json" }
        });
      }

      // ✅ Cancel Booking
      if (method === "DELETE" && url.pathname.startsWith("/api/cancel-booking")) {
        if (!currentUser) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });

        const pathParts = url.pathname.split("/");
        const location = decodeURIComponent(pathParts[3]);
        const date = decodeURIComponent(pathParts[4]);
        const time = decodeURIComponent(pathParts[5]);

        await env.DB.prepare(
          "DELETE FROM bookings WHERE email = ? AND location = ? AND date = ? AND time = ?"
        ).bind(currentUser.email, location, date, time).run();

        return new Response(JSON.stringify({ message: "Booking canceled!" }), {
          headers: { "Content-Type": "application/json" }
        });
      }

      // ✅ Create Stripe Checkout Session
      if (method === "POST" && url.pathname === "/api/create-checkout-session") {
        const { amount, email, date, time, duration, location } = await request.json();
        try {
          const session = await stripe.checkout.sessions.create({
            payment_method_types: ["card"],
            mode: "payment",
            success_url: "https://thatgolfplace.com/payment-success",
            cancel_url: "https://thatgolfplace.com/payment-cancel",
            line_items: [{
              price_data: { currency: "usd", product_data: { name: "Golf Booking" }, unit_amount: amount },
              quantity: 1
            }],
            metadata: { email, date, time, location, duration },
          });

          return new Response(JSON.stringify({ checkout_url: session.url }), { headers: { "Content-Type": "application/json" } });
        } catch (error) {
          return new Response(JSON.stringify({ error: "Error creating Stripe session" }), { status: 500 });
        }
      }

      return new Response("Not Found", { status: 404 });

    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  },
};
