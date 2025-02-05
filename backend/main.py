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

# Store booked slots with EPOCH timestamps
booked_slots: Dict[str, List[dict]] = {}

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

# API to return only valid time slots
@app.get("/api/booked-slots")
async def get_available_slots(date: str = Query(...)):
    """Returns only available (unbooked) slots for a given date"""
    all_slots = generate_time_slots()
    
    booked_times = set()
    for booking in booked_slots.get(date, []):
        start_epoch = booking["epoch_start"]
        end_epoch = start_epoch + int(booking["duration"] * 3600)  # Convert hours to seconds
        
        # Block out every time slot between start and end
        current_time = start_epoch
        while current_time < end_epoch:
            booked_times.add(current_time)
            current_time += 1800  # Increment by 30 min (1800 seconds)

    # Remove booked slots from available slots
    available_slots = []
    for slot in all_slots:
        epoch_time = convert_to_epoch(date, slot)
        if epoch_time not in booked_times:
            available_slots.append(slot)

    print(f"🚀 DEBUG: Booked Epoch Times: {booked_times}")
    print(f"✅ DEBUG: Available Slots: {available_slots}")

    return {"availableSlots": available_slots}

# Booking API (Now uses Epoch Timestamps)
@app.post("/api/book")
async def book_slot(
    date: str = Form(...),
    time: str = Form(...),
    duration: float = Form(...)
):
    """Book a time slot if it's available"""
    
    if date not in booked_slots:
        booked_slots[date] = []

    epoch_start = convert_to_epoch(date, time)
    
    for booking in booked_slots[date]:
        existing_start = booking["epoch_start"]
        existing_end = existing_start + int(booking["duration"] * 3600)

        if epoch_start < existing_end:
            raise HTTPException(status_code=400, detail="Time slot is already booked")

    booked_slots[date].append({"date": date, "time": time, "duration": duration, "epoch_start": epoch_start})
    
    print(f"✅ DEBUG: Stored Booking -> {booked_slots[date]}")

    return {"message": "Booking successful"}
