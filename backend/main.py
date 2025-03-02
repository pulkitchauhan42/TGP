import stripe
import os
from fastapi import FastAPI, HTTPException, Query, Form, Depends, Body, APIRouter, Request
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
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
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

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


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

def add_booking_to_slots(email: str, location: str, date: str, time: str, duration: float):
    """Helper function to add a booking to the booked_slots dictionary after payment"""
    
    # Ensure the location exists in the dictionary
    if location not in booked_slots:
        booked_slots[location] = {}
    
    # Ensure the date exists for the location
    if date not in booked_slots[location]:
        booked_slots[location][date] = []

    # Convert time to epoch
    epoch_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p").timestamp()

    # Check if the time slot is already booked
    epoch_end = epoch_start + int(duration * 3600)
    for booking in booked_slots[location][date]:
        existing_start = booking["epoch_start"]
        existing_end = existing_start + int(booking["duration"] * 3600)
        if not (epoch_end <= existing_start or epoch_start >= existing_end):
            raise HTTPException(status_code=400, detail="Time slot is already booked")

    # Add the new booking
    new_booking = {
        "email": email,
        "location": location,
        "date": date,
        "time": time,
        "duration": duration,
        "epoch_start": epoch_start,
        "confirmed": True,  # Mark as confirmed
    }

    booked_slots[location][date].append(new_booking)
    #print(f"✅ Booking added to booked_slots for {email} on {date} at {time}")

# ✅ Get User's Bookings
@app.get("/api/my-bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Retrieve all bookings for the current logged-in user"""
    user_email = current_user["email"]
    user_bookings = []

    if not booked_slots:
        raise HTTPException(status_code=404, detail="No bookings found")

    for location, dates in booked_slots.items():
        for date, bookings in dates.items():
            for booking in bookings:
                if booking["email"] == user_email:
                    user_bookings.append({
                        "location": booking["location"],
                        "date": booking["date"],
                        "time": booking["time"],
                        "duration": booking["duration"],
                    })

    if not user_bookings:
        raise HTTPException(status_code=404, detail="No bookings found")

    return {"bookings": user_bookings}


# ✅ Create a test member with 50 allocated hours
users_db["member@example.com"] = {
    "email": "member@example.com",
    "hashed_password": hash_password("password123"),
    "full_name": "Example Member",
    "is_member": True,
    "member_hours": 1.0,
}

users_db["p@tgp.com"] = {
    "email": "p@tgp.com",
    "hashed_password": hash_password("p"),
    "full_name": "Example Non-Member",
    "is_member": False,
    "member_hours": 0,
}

# ✅ Pydantic Models
class PaymentRequest(BaseModel):
    date: str
    time: str
    duration: float
    location: str
    email: EmailStr
    amount: int

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
        # Validate the incoming data
        print(f"Payment data received: {payment_data}")  # Debugging

        # Ensure the amount is an integer (in cents)
        if not payment_data.amount:
            raise HTTPException(status_code=400, detail="Amount is required")

        # Create the Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            success_url="http://localhost:8081/payment-success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8081/payment-cancel",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "Golf Simulator Booking",
                            "description": f"Booking on {payment_data.date} at {payment_data.time} for {payment_data.duration} hour(s)"
                        },
                        "unit_amount": payment_data.amount,  # Ensure amount is in cents
                    },
                    "quantity": 1,
                }
            ],
            metadata={
                "email": payment_data.email,
                "date": payment_data.date,
                "time": payment_data.time,
                "location": payment_data.location,
                #"duration": "1.0",
                "duration": str(payment_data.duration),
            },
        )

        return JSONResponse({"checkout_url": session.url})

    except Exception as e:
        print(f"Error creating Stripe session: {e}")
        raise HTTPException(status_code=500, detail="Error creating Stripe session.")




# Handle Stripe webhook events
@app.post("/api/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return {"error": "Invalid payload"}
    except stripe.error.SignatureVerificationError as e:
        return {"error": "Invalid signature"}

    # Handle checkout.session.completed (Payment Success)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Ensure the metadata contains email and use it
        email = session.get("customer_email", None)  # Retrieve email directly if available
        if not email:
            email = session["metadata"].get("email", None)  # Retrieve from metadata if not in customer_email

        if not email:
            raise HTTPException(status_code=400, detail="Email not found in session data")

        booking_date = session["metadata"]["date"]
        booking_time = session["metadata"]["time"]
        booking_duration = float(session["metadata"]["duration"])
        location = session["metadata"]["location"]

        # Proceed to deduct hours and add booking to slots
        try:
            user = users_db.get(email)
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")

            if user["is_member"]:
                # Deduct hours if the user is a member
                remaining_duration = booking_duration - user["member_hours"]
                if remaining_duration > 0:
                    # Deduct the paid amount for the hours
                    users_db[email]["member_hours"] -= booking_duration  # Update member hours

                    if users_db[email]["member_hours"] < 0:
                        users_db[email]["member_hours"] = 0  # Set to 0 if it goes negative

            # Add the booking to booked_slots
            add_booking_to_slots(email, location, booking_date, booking_time, booking_duration)

            return {"status": "success"}
        except HTTPException as e:
            return {"error": f"Error adding booking: {e.detail}"}

    # Handle other events like payment failure or expiration if necessary

    return {"status": "success"}


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

@app.get("/api/booked-slots")
async def get_booked_slots(
    date: str = Query(..., description="Date of the booking (YYYY-MM-DD)"),
    location: str = Query(DEFAULT_LOCATION, description="Location of the booking")
):
    """Returns booked and available slots for a given date at a selected location."""
    
    print(f"🔍 Incoming request: date={date}, location={location}")  # Debugging

    # Define all available time slots (4:00 AM - 3:30 AM)
    all_slots = [
        f"{hour % 12 if hour % 12 else 12}:{minute} {'AM' if hour < 12 else 'PM'}"
        for hour in list(range(4, 24)) + [0, 1, 2, 3]
        for minute in ["00", "30"]
    ]

    # Initialize location if missing
    if location not in booked_slots:
        booked_slots[location] = {}

    booked_times = set()

    # Store booked slots for the given date
    if date in booked_slots[location]:
        for booking in booked_slots[location][date]:
            start_epoch = booking["epoch_start"]
            end_epoch = start_epoch + int(booking["duration"] * 3600)

            current_time = start_epoch
            while current_time < end_epoch:
                booked_times.add(current_time)
                current_time += 1800  # Move in 30-minute increments

    now_epoch = int(datetime.now().timestamp())

    # Generate available slots by filtering out booked times
    available_slots = [
        slot for slot in all_slots
        if datetime.strptime(f"{date} {slot}", "%Y-%m-%d %I:%M %p").timestamp() not in booked_times
        and datetime.strptime(f"{date} {slot}", "%Y-%m-%d %I:%M %p").timestamp() > now_epoch
    ]

    return {
        "bookedSlots": list(booked_times),  # Return all booked time slots
        "availableSlots": available_slots
    }

# 🔹 **Retrieve User's Bookings**
@app.get("/api/my-bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Retrieve all bookings for the current logged-in user"""
    user_email = current_user["email"]
    user_bookings = []

    if not booked_slots:
        raise HTTPException(status_code=404, detail="No bookings found")

    for location, dates in booked_slots.items():
        for date, bookings in dates.items():
            for booking in bookings:
                if booking["email"] == user_email:
                    user_bookings.append({
                        "location": booking["location"],
                        "date": booking["date"],
                        "time": booking["time"],
                        "duration": booking["duration"],
                    })

    if not user_bookings:
        raise HTTPException(status_code=404, detail="No bookings found")
    print(f"✅ Bookings found for {user_email}: {user_bookings}")
    return {"bookings": user_bookings}


@app.delete("/api/cancel-booking/{location}/{date}/{time}")
async def cancel_booking(
    location: str,
    date: str,
    time: str,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a booking (24 hours in advance only)"""
    
    # Search for the booking in the booked_slots dictionary for the specific location and date
    found_booking = None
    for booking in booked_slots.get(location, {}).get(date, []):
        if booking["email"] == current_user["email"] and booking["time"] == time:
            found_booking = booking
            break
    
    # If booking is not found, return 404
    if not found_booking:
        raise HTTPException(status_code=404, detail="Booking not found for this time slot.")
    
    # Check if the booking is at least 24 hours in advance
    epoch_start = found_booking["epoch_start"]
    current_epoch = int(datetime.now().timestamp())
    if epoch_start - current_epoch < 86400:  # Less than 24 hours in advance
        raise HTTPException(
            status_code=400,
            detail="Cancellations are only allowed 24 hours in advance"
        )

    # Remove the booking from the booked slots
    booked_slots[location][date].remove(found_booking)

    # If the user is a member, refund their allocated hours
    if current_user["is_member"]:
        users_db[current_user["email"]]["member_hours"] += found_booking["duration"]
        print(f"✅ Member hours refunded. New balance: {users_db[current_user['email']]['member_hours']}")

    return {"message": "Booking successfully cancelled"}
app.include_router(router)

@app.post("/api/book")
async def book_slot(
    date: str = Form(...),
    time: str = Form(...),
    duration: float = Form(...),
    location: str = Form(DEFAULT_LOCATION),
    current_user: dict = Depends(get_current_user)
):
    """Book a time slot at the default location if it's available"""
    print(f"📌 DEBUG: Booking attempt by {current_user['email']} for {date} at {time} ({duration} hours)")

    now_epoch = int(datetime.now().timestamp())
    epoch_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p").timestamp()

    if epoch_start < now_epoch:
        raise HTTPException(status_code=400, detail="Cannot book a past time.")

    if location not in booked_slots:
        booked_slots[location] = {}

    if date not in booked_slots[location]:
        booked_slots[location][date] = []

    epoch_end = epoch_start + int(duration * 3600)
    for booking in booked_slots[location][date]:
        existing_start = booking["epoch_start"]
        existing_end = existing_start + int(booking["duration"] * 3600)
        if not (epoch_end <= existing_start or epoch_start >= existing_end):
            raise HTTPException(status_code=400, detail="Time slot is already booked")

    if current_user["is_member"]:
        if current_user["member_hours"] >= duration:
            users_db[current_user["email"]]["member_hours"] -= duration
            print(f"✅ DEBUG: {current_user['email']} booked using credits. Remaining: {users_db[current_user['email']]['member_hours']}")

            new_booking = {
                "email": current_user["email"],
                "location": location,
                "date": date,
                "time": time,
                "duration": duration,
                "epoch_start": epoch_start,
            }

            booked_slots[location][date].append(new_booking)

            return {
                "message": "Booking successful without payment.",
                "redirect_to_payment": False,
                "new_booking": new_booking
            }
        else:
            remaining_duration = duration - current_user["member_hours"]
            print(remaining_duration)
            remaining_amount = remaining_duration * 50 * 100  # Convert to cents
            
            return {
                "message": "You don't have enough hours to complete this booking.",
                "redirect_to_payment": True,
                "amount_to_pay": remaining_amount,
                "available_hours": current_user["member_hours"],
                "stripe_session_url": "/payment/member-payment"
            }

    else:
        remaining_amount = duration * 50 * 100  # Full price for non-members in cents
        
        return {
            "message": "You need to pay to complete the booking.",
            "redirect_to_payment": True,
            "amount_to_pay": remaining_amount,
            "stripe_session_url": "/payment/non-member-payment"
        }
