import jwt from "jsonwebtoken";

const SECRET_KEY = "secret"; // Replace with a secure key
const users_db = {
  "member@example.com": {
    email: "member@example.com",
    hashed_password: "$argon2id$v=19$m=65536,t=3,p=4$8p8...$Y...",
    full_name: "Example Member",
    is_member: true,
    member_hours: 10.0,
  },
};

export async function signup(request) {
  const { email, password, full_name, is_member, member_hours } = await request.json();

  if (users_db[email]) {
    return new Response(JSON.stringify({ error: "User already exists" }), { status: 400 });
  }

  const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: "1h" });

  users_db[email] = {
    email,
    full_name,
    hashed_password: password, // TODO: Hash passwords properly
    is_member,
    member_hours,
  };

  return new Response(JSON.stringify({ message: "User registered successfully!", token, is_member }), {
    headers: { "Content-Type": "application/json" },
  });
}

export async function login(request) {
  const { email, password } = await request.json();

  if (!users_db[email] || users_db[email].hashed_password !== password) {
    return new Response(JSON.stringify({ error: "Invalid credentials" }), { status: 400 });
  }

  const token = jwt.sign({ sub: email }, SECRET_KEY, { expiresIn: "1h" });

  return new Response(JSON.stringify({ access_token: token, token_type: "bearer", is_member: users_db[email].is_member }), {
    headers: { "Content-Type": "application/json" },
  });
}
