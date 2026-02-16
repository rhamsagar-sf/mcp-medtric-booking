from typing import Any

from fastmcp import FastMCP

from service_api import ServiceAPIClient, ServiceAPIError

mcp = FastMCP("My Server")


@mcp.tool
def get_service_assistant_availability(
    postal_code: str,
    preferred_date: str,
    service_type: str,
    timezone: str = "America/Chicago",
    product_id: str = "",
) -> dict[str, Any]:
    """Get service assistant availability from the downstream scheduling API."""
    payload = {
        "postal_code": postal_code,
        "preferred_date": preferred_date,
        "service_type": service_type,
        "timezone": timezone,
    }
    if product_id.strip():
        payload["product_id"] = product_id

    try:
        data = ServiceAPIClient().get_service_assistant_availability(payload)
    except ServiceAPIError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "data": data}


@mcp.tool
def book_service_visit(
    customer_name: str,
    customer_phone: str,
    service_type: str,
    slot_id: str,
    address_line1: str,
    city: str,
    state: str,
    postal_code: str,
    customer_email: str = "",
    notes: str = "",
) -> dict[str, Any]:
    """Book a service visit with selected slot and customer/address details."""
    payload = {
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "service_type": service_type,
        "slot_id": slot_id,
        "address": {
            "line1": address_line1,
            "city": city,
            "state": state,
            "postal_code": postal_code,
        },
    }
    if customer_email.strip():
        payload["customer_email"] = customer_email
    if notes.strip():
        payload["notes"] = notes

    try:
        data = ServiceAPIClient().book_service_visit(payload)
    except ServiceAPIError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "data": data}


@mcp.tool
def reschedule_booking(
    booking_id: str,
    new_slot_id: str,
    reason: str = "",
) -> dict[str, Any]:
    """Reschedule an existing service booking to a new slot."""
    payload = {
        "booking_id": booking_id,
        "new_slot_id": new_slot_id,
    }
    if reason.strip():
        payload["reason"] = reason

    try:
        data = ServiceAPIClient().reschedule_booking(payload)
    except ServiceAPIError as exc:
        return {"ok": False, "error": str(exc)}
    return {"ok": True, "data": data}


@mcp.resource("service://capabilities")
def capabilities() -> str:
    return (
        "Service Assistant Scheduler capabilities:\n"
        "1. Get Service Assistant Availability\n"
        "2. Book Service Visit\n"
        "3. Reschedule Booking"
    )


if __name__ == "__main__":
    mcp.run()
