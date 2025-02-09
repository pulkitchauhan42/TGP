import stripe
import os
from fastapi import FastAPI, HTTPException, Query, Form, Depends, Body, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from argon2 import PasswordHasher
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

# ✅ Stripe API Key Setup (Fixed Env Variable)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Password Hashing & OAuth2 Scheme (Using Argon2)
ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# ✅ Simulated Databases
users_db: Dict[str, dict] = {}  # Stores users
booked_slots: Dict[str, Dict[str, List[dict]]] = {}  # Stores bookings

DEFAULT_LOCATION = "That Golf Place - Main Location"

# ✅ Helper Functions
def hash_password(password: str):
    """Hash password using Argon2"""
    return ph.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify password using Argon2"""
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False  # Invalid password
def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    """Generate JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "your_secret_key_here", algorithm="HS256")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Authenticate user via JWT token"""
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, "your_secret_key_here", algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None or email not in users_db:
            raise credentials_exception
        return users_db[email]
    except JWTError:
        raise credentials_exception

# ✅ Create a test member with 50 allocated hours
users_db["member@example.com"] = {
    "email": "member@example.com",
    "hashed_password": hash_password("password123"),
    "full_name": "Example Member",
    "is_member": True,
    "member_hours": 50.0,
}

# ✅ Pydantic Models
class PaymentRequest(BaseModel):
    date: str
    time: str
    duration: float
    location: str
    email: EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    is_member: bool = False
    member_hours: float = 0.0

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# ✅ Signup - Returns JWT Token
@app.post("/api/signup")
async def signup(
    email: EmailStr = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    is_member: bool = Form(False),
    member_hours: float = Form(0.0)
):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    users_db[email] = {
        "email": email,
        "full_name": full_name,
        "hashed_password": hashed_password,
        "is_member": is_member,
        "member_hours": member_hours,
    }

    token = create_jwt_token({"sub": email})
    return {"message": "User registered successfully!", "token": token, "is_member": is_member}

# ✅ Stripe Checkout Session
@router.post("/api/create-checkout-session")
async def create_checkout_session(payment_data: PaymentRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            success_url="http://localhost:5173/payment-success",
            cancel_url="http://localhost:5173/payment-cancel",
            customer_email=payment_data.email,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Golf Simulator Booking",
                            "description": f"Booking on {payment_data.date} at {payment_data.time} for {payment_data.duration} hours"
                        },
                        "unit_amount": int(30 * payment_data.duration * 100),
                    },
                    "quantity": 1,
                }
            ],
            metadata={"email": payment_data.email, "date": payment_data.date, "time": payment_data.time},
        )
        return JSONResponse({"checkout_url": session.url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
app.include_router(router)

# ✅ User Login
@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_jwt_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer", "is_member": user["is_member"]}

# ✅ Fetch User Profile
@app.get("/api/me")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    return {
        "full_name": current_user["full_name"],
        "email": current_user["email"],
        "is_member": current_user["is_member"],
        "member_hours": current_user["member_hours"] if current_user["is_member"] else 0
    }

# ✅ Update User Profile
@app.put("/api/update-user")
async def update_user_profile(
    full_name: Optional[str] = Form(None),
    new_password: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]

    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    if full_name:
        users_db[email]["full_name"] = full_name
    if new_password:
        users_db[email]["hashed_password"] = hash_password(new_password)

    return {"message": "Profile updated successfully!"}

# ✅ Book a Slot
@app.post("/api/book")
async def book_slot(
    date: str = Form(...),
    time: str = Form(...),
    duration: float = Form(...),
    location: str = Form(DEFAULT_LOCATION),
    current_user: dict = Depends(get_current_user)
):
    now_epoch = int(datetime.now().timestamp())
    epoch_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p").timestamp()
    if epoch_start < now_epoch:
        raise HTTPException(status_code=400, detail="Cannot book a past time.")

    if current_user["is_member"] and current_user["member_hours"] < duration:
        raise HTTPException(status_code=400, detail="Not enough allocated hours.")

    new_booking = {
        "email": current_user["email"],
        "location": location,
        "date": date,
        "time": time,
        "duration": duration,
        "epoch_start": epoch_start,
    }
    booked_slots.setdefault(location, {}).setdefault(date, []).append(new_booking)

    return {"message": "Booking successful"}
