# silverscisor-python/routers/service_requests.py

import json
import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["Service Requests"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STORE_PATH = os.path.join(DATA_DIR, "service_requests.json")

SALON_SERVICE_URL = os.getenv("SALON_SERVICE_URL", "http://localhost:5002/api")


# === Pydantic Schemas ===

class ServiceRequestCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: Optional[str] = ""
    service_type: str  # haircuts, beardStyles, hairColors
    service_id: int
    service_name: str
    service_price: int
    service_duration: Optional[str] = "30 min"
    face_shape: Optional[str] = ""
    skin_tone: Optional[str] = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ServiceRequestAccept(BaseModel):
    salon_id: str
    salon_name: str
    salon_phone: Optional[str] = ""


class ServiceRequestSchedule(BaseModel):
    salon_id: str
    date: str
    time_slot: str
    notes: Optional[str] = ""


# === File-based Store ===

def _load_requests():
    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return []


def _save_requests(requests):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(requests, f, indent=2, ensure_ascii=False)


# === Socket.IO notification helper ===

def _notify_salons_via_salon_service(event_type: str, payload: dict):
    try:
        import httpx
        with httpx.Client(timeout=3) as client:
            client.post(
                f"{SALON_SERVICE_URL}/notify-salons",
                json={"event": event_type, "data": payload},
            )
    except Exception as e:
        print(f"[ServiceRequest] Salon-service notify skipped: {e}")


# === Endpoints ===

@router.get("/service-requests")
async def list_requests(
    status: Optional[str] = Query(None, description="Filter by status: pending, accepted, scheduled, cancelled"),
    salon_id: Optional[str] = Query(None, description="Filter by salon that accepted"),
):
    requests = _load_requests()
    if status:
        requests = [r for r in requests if r.get("status") == status]
    if salon_id:
        requests = [
            r for r in requests
            if r.get("accepted_by") and r["accepted_by"].get("salon_id") == salon_id
        ]
    return {"success": True, "count": len(requests), "data": requests}


@router.get("/service-requests/{request_id}")
async def get_request(request_id: str):
    requests = _load_requests()
    for r in requests:
        if r["id"] == request_id:
            return {"success": True, "data": r}
    raise HTTPException(status_code=404, detail="Service request not found")


@router.post("/service-requests")
async def create_request(req: ServiceRequestCreate):
    requests = _load_requests()

    new_req = {
        "id": str(uuid.uuid4()),
        "status": "pending",
        "customer_name": req.customer_name,
        "customer_phone": req.customer_phone,
        "customer_email": req.customer_email,
        "service_type": req.service_type,
        "service_id": req.service_id,
        "service_name": req.service_name,
        "service_price": req.service_price,
        "service_duration": req.service_duration,
        "face_shape": req.face_shape,
        "skin_tone": req.skin_tone,
        "latitude": req.latitude,
        "longitude": req.longitude,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "accepted_by": None,
        "scheduled_date": None,
        "scheduled_time": None,
        "notes": None,
        "booking_id": None,
    }

    requests.insert(0, new_req)
    _save_requests(requests)

    _notify_salons_via_salon_service("new_service_request", {
        "request_id": new_req["id"],
        "service_name": req.service_name,
        "service_type": req.service_type,
        "customer_name": req.customer_name,
        "latitude": req.latitude,
        "longitude": req.longitude,
    })

    return {
        "success": True,
        "data": new_req,
        "message": "Service request created! Nearby salons have been notified.",
    }


@router.post("/service-requests/{request_id}/accept")
async def accept_request(request_id: str, req: ServiceRequestAccept):
    requests = _load_requests()
    for r in requests:
        if r["id"] == request_id:
            if r["status"] != "pending":
                raise HTTPException(
                    status_code=400,
                    detail=f"Request already {r['status']}. Only pending requests can be accepted.",
                )

            r["status"] = "accepted"
            r["accepted_by"] = {
                "salon_id": req.salon_id,
                "salon_name": req.salon_name,
                "salon_phone": req.salon_phone,
                "accepted_at": datetime.now().isoformat(),
            }
            r["updated_at"] = datetime.now().isoformat()
            _save_requests(requests)

            _notify_salons_via_salon_service("request_accepted", {
                "request_id": request_id,
                "salon_name": req.salon_name,
                "customer_name": r["customer_name"],
            })

            return {
                "success": True,
                "data": r,
                "message": f"Request accepted by {req.salon_name}! Now please schedule a time slot.",
            }

    raise HTTPException(status_code=404, detail="Service request not found")


@router.post("/service-requests/{request_id}/schedule")
async def schedule_request(request_id: str, req: ServiceRequestSchedule):
    requests = _load_requests()
    for r in requests:
        if r["id"] == request_id:
            if r["status"] != "accepted":
                raise HTTPException(
                    status_code=400,
                    detail=f"Request must be accepted first. Current status: {r['status']}",
                )

            if not r["accepted_by"] or r["accepted_by"]["salon_id"] != req.salon_id:
                raise HTTPException(
                    status_code=400,
                    detail="Only the accepting salon can schedule this request",
                )

            r["status"] = "scheduled"
            r["scheduled_date"] = req.date
            r["scheduled_time"] = req.time_slot
            r["notes"] = req.notes
            r["updated_at"] = datetime.now().isoformat()

            booking_id = None
            try:
                import httpx
                with httpx.Client(timeout=5) as client:
                    booking_res = client.post(
                        f"{SALON_SERVICE_URL}/bookings",
                        json={
                            "userId": "",
                            "salonId": r["accepted_by"]["salon_id"],
                            "customerName": r["customer_name"],
                            "customerPhone": r["customer_phone"],
                            "service": {
                                "serviceId": r["service_id"],
                                "name": r["service_name"],
                                "price": r["service_price"],
                                "estimatedDuration": r.get("service_duration", "30 min"),
                            },
                            "date": req.date,
                            "timeSlot": req.time_slot,
                        },
                    )
                    if booking_res.status_code == 201:
                        booking_data = booking_res.json()
                        booking_id = booking_data.get("data", {}).get("_id")
            except Exception as e:
                print(f"[ServiceRequest] Salon-service booking creation failed: {e}")

            r["booking_id"] = booking_id
            _save_requests(requests)

            return {
                "success": True,
                "data": r,
                "message": (
                    f"Appointment scheduled for {req.date} at {req.time_slot}. "
                    f"Customer {r['customer_name']} has been notified via WhatsApp."
                ),
                "booking_created": booking_id is not None,
            }

    raise HTTPException(status_code=404, detail="Service request not found")


@router.post("/service-requests/{request_id}/cancel")
async def cancel_request(request_id: str):
    requests = _load_requests()
    for r in requests:
        if r["id"] == request_id:
            if r["status"] in ("cancelled", "scheduled"):
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot cancel request with status: {r['status']}",
                )
            r["status"] = "cancelled"
            r["updated_at"] = datetime.now().isoformat()
            _save_requests(requests)

            _notify_salons_via_salon_service("request_cancelled", {
                "request_id": request_id,
                "customer_name": r["customer_name"],
            })

            return {"success": True, "message": "Service request cancelled"}
    raise HTTPException(status_code=404, detail="Service request not found")
