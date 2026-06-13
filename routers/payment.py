# silverscisor-python/routers/payment.py

import os
import json
import razorpay
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["Payment"])

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")
ANALYSIS_PRICE = int(os.getenv("ANALYSIS_PRICE", 10))  # ₹10 per analysis

# Razorpay client (only if keys available)
client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


class CreateOrderRequest(BaseModel):
    pass


class CreateOrderResponse(BaseModel):
    success: bool
    orderId: str
    amount: int
    currency: str
    keyId: str = ""


class VerifyPaymentRequest(BaseModel):
    razorpayOrderId: str
    razorpayPaymentId: str
    razorpaySignature: str


class VerifyPaymentResponse(BaseModel):
    success: bool


@router.post("/create-order", response_model=CreateOrderResponse)
async def create_order():
    try:
        amount_paisa = ANALYSIS_PRICE * 100  # ₹X * 100 = paise

        if client:
            order = client.order.create({
                "amount": amount_paisa,
                "currency": "INR",
                "receipt": "analysis_receipt",
                "payment_capture": 1
            })
            return CreateOrderResponse(
                success=True,
                orderId=order["id"],
                amount=amount_paisa,
                currency="INR",
                keyId=RAZORPAY_KEY_ID
            )
        else:
            # Test mode — mock order
            return CreateOrderResponse(
                success=True,
                orderId="order_test_" + os.urandom(8).hex(),
                amount=amount_paisa,
                currency="INR",
                keyId="rzp_test_placeholder"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")


@router.post("/verify-payment", response_model=VerifyPaymentResponse)
async def verify_payment(req: VerifyPaymentRequest):
    try:
        if client:
            params_dict = {
                "razorpay_order_id": req.razorpayOrderId,
                "razorpay_payment_id": req.razorpayPaymentId,
                "razorpay_signature": req.razorpaySignature,
            }
            client.utility.verify_payment_signature(params_dict)
        # else: test mode — always valid
        return VerifyPaymentResponse(success=True)
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Payment verification failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Verification error: {str(e)}")
