from datetime import datetime, timedelta
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Mock Service API", version="0.1.0")

BOOKINGS: dict[str, dict] = {}


class AvailabilityRequest(BaseModel):
    postal_code: str
    preferred_date: str
    service_type: str
    timezone: str = "America/Chicago"
    product_id: str | None = None


class BookingAddress(BaseModel):
    line1: str
    city: str
    state: str
    postal_code: str


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    service_type: str
    slot_id: str
    address: BookingAddress
    customer_email: str | None = None
    notes: str | None = None


class RescheduleRequest(BaseModel):
    booking_id: str
    new_slot_id: str
    reason: str | None = None


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/service-assistant/availability")
def service_assistant_availability(req: AvailabilityRequest) -> dict:
    try:
        start = datetime.fromisoformat(req.preferred_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="preferred_date must be ISO-8601")

    slots = []
    for i in range(3):
        slot_start = start + timedelta(hours=i * 2)
        slot_end = slot_start + timedelta(hours=1)
        slot_id = f"{req.postal_code}-{slot_start.strftime('%Y%m%d%H%M')}"
        slots.append(
            {
                "slot_id": slot_id,
                "start_time": slot_start.isoformat(),
                "end_time": slot_end.isoformat(),
                "technician_level": "L2",
            }
        )

    return {
        "service_type": req.service_type,
        "postal_code": req.postal_code,
        "timezone": req.timezone,
        "slots": slots,
    }


@app.post("/service-visits/book")
def service_visits_book(req: BookingRequest) -> dict:
    booking_id = str(uuid4())
    confirmation = f"CNF-{booking_id[:8].upper()}"

    BOOKINGS[booking_id] = {
        "booking_id": booking_id,
        "confirmation_number": confirmation,
        "status": "BOOKED",
        "slot_id": req.slot_id,
        "customer_name": req.customer_name,
        "customer_phone": req.customer_phone,
        "customer_email": req.customer_email,
        "service_type": req.service_type,
        "address": req.address.model_dump(),
        "notes": req.notes,
    }

    return BOOKINGS[booking_id]


@app.post("/service-visits/reschedule")
def service_visits_reschedule(req: RescheduleRequest) -> dict:
    booking = BOOKINGS.get(req.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking_id not found")

    booking["slot_id"] = req.new_slot_id
    booking["status"] = "RESCHEDULED"
    booking["reschedule_reason"] = req.reason
    booking["updated_at"] = datetime.utcnow().isoformat() + "Z"
    return booking
