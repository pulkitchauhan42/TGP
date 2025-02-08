from fastapi import FastAPI, HTTPException, Query, Form, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from jose import jwt, JWTError
from pydantic import BaseModel, EmailStr

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 JWT Authentication Settings
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔹 Password Hashing & OAuth2 Scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# 🔹 Simulated Databases
users_db: Dict[str, dict] = {}  # Stores users
booked_slots: Dict[str, Dict[str, List[dict]]] = {}  # Stores bookings

DEFAULT_LOCATION = "That Golf Place - Main Location"

# 🔹 Helper Functions
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Authenticate user via JWT token"""
    credentials_exception = HTTPException(
        status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None or email not in users_db:
            raise credentials_exception
        return users_db[email]
    except JWTError:
        raise credentials_exception

# Create a test member with 50 allocated hours
users_db["member@example.com"] = {
    "email": "member@example.com",
    "hashed_password": hash_password("password123"),  # Pre-hash password
    "full_name": "Example Member",
    "is_member": True,
    "member_hours": 50.0,  # Allocate 50 hours for testing
}


# 🔹 Pydantic Models
class User(BaseModel):
    email: EmailStr
    password: str
    is_member: bool = False
    member_hours: float = 0.0  # Members get allocated hours

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None





# ✅ Modify signup to return a JWT token
@app.post("/api/signup")
async def signup(
    email: EmailStr = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),  # New field for Full Name
    is_member: bool = Form(False),
    member_hours: float = Form(0.0)
):
    if email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(password)
    users_db[email] = {
        "email": email,
        "full_name": full_name,  # Store full name
        "hashed_password": hashed_password,
        "is_member": is_member,
        "member_hours": member_hours,
    }

    # ✅ Generate token upon signup
    token = create_jwt_token({"sub": email})

    return {"message": "User registered successfully!", "token": token, "is_member": is_member}



# 🔹 **User Login**
@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print(f"🟢 DEBUG: Logging in user {user['email']} (is_member={user['is_member']})")

    token = create_jwt_token({"sub": user["email"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "is_member": user["is_member"]
    }


# 🔹 **Fetch User Profile**
@app.get("/api/me")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Returns authenticated user profile"""
    return {
        "email": current_user["email"],
        "is_member": current_user["is_member"],
        "member_hours": current_user["member_hours"] if current_user["is_member"] else 0  # Non-members see 0
    }

# 🛠️ DEBUGGING: Modify /api/book to Ensure It Saves the Booking Correctly
@app.post("/api/book")
async def book_slot(
    date: str = Form(...),
    time: str = Form(...),
    duration: float = Form(...),
    location: str = Form(DEFAULT_LOCATION),
    current_user: dict = Depends(get_current_user)
):
    """Book a time slot at the default location if it's available"""
    now_epoch = int(datetime.now().timestamp())
    epoch_start = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p").timestamp()

    if epoch_start < now_epoch:
        raise HTTPException(status_code=400, detail="Cannot book a past time.")

    if location not in booked_slots:
        booked_slots[location] = {}

    if date not in booked_slots[location]:
        booked_slots[location][date] = []

    epoch_end = epoch_start + int(duration * 3600)

    # **Check for overlapping bookings**
    for booking in booked_slots[location][date]:
        existing_start = booking["epoch_start"]
        existing_end = existing_start + int(booking["duration"] * 3600)

        if not (epoch_end <= existing_start or epoch_start >= existing_end):
            raise HTTPException(status_code=400, detail="Time slot is already booked")

    # **Check if Member has Enough Hours**
    if current_user["is_member"]:
        print(f"🟢 DEBUG: Before booking, {current_user['email']} has {current_user['member_hours']} hours")

        if current_user["member_hours"] < duration:
            raise HTTPException(status_code=400, detail="Not enough allocated hours for booking.")

        users_db[current_user["email"]]["member_hours"] -= duration  # Deduct hours

        print(f"🟢 DEBUG: After booking, {current_user['email']} now has {users_db[current_user['email']]['member_hours']} hours left")

    # **Store the Booking & Associate it with the User**
    new_booking = {
        "email": current_user["email"],
        "location": location,
        "date": date,
        "time": time,
        "duration": duration,
        "epoch_start": epoch_start,
    }
    
    booked_slots[location][date].append(new_booking)

    print(f"✅ DEBUG: Booking successfully added -> {new_booking}")

    return {
        "message": "Booking successful",
        "remaining_hours": users_db[current_user["email"]]["member_hours"]
    }


# 🔹 **Fix `/api/my-bookings` to Properly Retrieve User Bookings**
@app.get("/api/my-bookings")
async def get_user_bookings(current_user: dict = Depends(get_current_user)):
    """Retrieve all bookings for the current logged-in user"""
    user_email = current_user["email"]
    user_bookings = []

    print(f"🟢 DEBUG: Checking bookings for {user_email}")  # Debugging

    # Ensure we look for bookings at all locations
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

    print(f"🟢 DEBUG: Bookings found: {user_bookings}")  # Debugging

    return {"bookings": user_bookings}


# 🔹 **Retrieve Available Slots**
@app.get("/api/booked-slots")
async def get_available_slots(date: str = Query(...), location: str = Query(DEFAULT_LOCATION)):
    """Returns available (unbooked) slots for a given date at the selected location"""
    
    all_slots = [
        f"{hour % 12 if hour % 12 else 12}:00 {'AM' if hour < 12 else 'PM'}"
        for hour in range(6, 23)
    ]

    if location not in booked_slots:
        booked_slots[location] = {}  # Ensure location exists

    booked_times = {booking["epoch_start"] for booking in booked_slots[location].get(date, [])}
    now_epoch = int(datetime.now().timestamp())

    available_slots = [
        slot for slot in all_slots 
        if datetime.strptime(f"{date} {slot}", "%Y-%m-%d %I:%M %p").timestamp() not in booked_times 
        and datetime.strptime(f"{date} {slot}", "%Y-%m-%d %I:%M %p").timestamp() > now_epoch
    ]

    return {"availableSlots": available_slots}
