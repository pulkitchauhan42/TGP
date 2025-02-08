from fastapi import FastAPI, HTTPException, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store booked slots per location
booked_slots: Dict[str, Dict[str, List[dict]]] = {}

# Default Location (Only One for Now)
DEFAULT_LOCATION = "That Golf Place - Main Location"

# Generate time slots (every 30 min from 6 AM to 10 PM)
def generate_time_slots():
    slots = []
    for hour in range(6, 22 + 1):
        slots.append(f"{hour % 12 if hour % 12 else 12}:00 {'AM' if hour < 12 else 'PM'}")
        slots.append(f"{hour % 12 if hour % 12 else 12}:30 {'AM' if hour < 12 else 'PM'}")
    return slots

# Convert Date & Time to Epoch
def convert_to_epoch(date: str, time: str):
    dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %I:%M %p")
    return int(dt.timestamp())

# API to return only valid time slots (Default Location)
@app.get("/api/booked-slots")
async def get_available_slots(date: str = Query(...), location: str = Query(DEFAULT_LOCATION)):
    """Returns available (unbooked) slots for a given date at the default location"""
    all_slots = generate_time_slots()

    # Ensure location exists in records
    if location not in booked_slots:
        booked_slots[location] = {}

    booked_times = set()
    for booking in booked_slots[location].get(date, []):
        start_epoch = booking["epoch_start"]
        end_epoch = start_epoch + int(booking["duration"] * 3600)

        # Block out every time slot between start and end
        current_time = start_epoch
        while current_time < end_epoch:
            booked_times.add(current_time)
            current_time += 1800  # Increment by 30 min (1800 seconds)

    # Remove booked slots from available slots
    available_slots = []
    now_epoch = int(datetime.now().timestamp())

    for slot in all_slots:
        epoch_time = convert_to_epoch(date, slot)

        if epoch_time not in booked_times and epoch_time > now_epoch:
            available_slots.append(slot)

    print(f"🚀 DEBUG: Booked Slots for {location} on {date}: {booked_times}")
    print(f"✅ DEBUG: Available Slots for {location} on {date}: {available_slots}")

    return {"availableSlots": available_slots}

# Booking API (Default Location)
@app.post("/api/book")
async def book_slot(
    date: str = Form(...),
    time: str = Form(...),
    duration: float = Form(...),
    location: str = Form(DEFAULT_LOCATION)  # Default to single location
):
    """Book a time slot at the default location if it's available"""
    now_epoch = int(datetime.now().timestamp())
    epoch_start = convert_to_epoch(date, time)

    if epoch_start < now_epoch:
        raise HTTPException(status_code=400, detail="Cannot book a past time.")

    if location not in booked_slots:
        booked_slots[location] = {}

    if date not in booked_slots[location]:
        booked_slots[location][date] = []

    # Check for overlapping bookings
    epoch_end = epoch_start + int(duration * 3600)

    for booking in booked_slots[location][date]:
        existing_start = booking["epoch_start"]
        existing_end = existing_start + int(booking["duration"] * 3600)

        if not (epoch_end <= existing_start or epoch_start >= existing_end):
            raise HTTPException(status_code=400, detail="Time slot is already booked")

    # Store the booking
    booked_slots[location][date].append({
        "date": date,
        "time": time,
        "duration": duration,
        "epoch_start": epoch_start
    })
    
    print(f"✅ DEBUG: Stored Booking at {location} -> {booked_slots[location][date]}")

    return {"message": "Booking successful", "location": location}
