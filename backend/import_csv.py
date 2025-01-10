# main.py

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models import Payment, PaymentResponse
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["adcore_payments"]
payments_collection = db["payments"]

# Test Connection Endpoint
@app.get("/test-connection")
async def test_connection():
    """Check if MongoDB is reachable by fetching a sample payment."""
    try:
        sample_payment = await payments_collection.find_one()
        if sample_payment:
            sample_payment["_id"] = str(sample_payment["_id"])  # Convert ObjectId to string
            return {"status": "connected", "sample_payment": sample_payment}
        else:
            return {"status": "connected", "sample_payment": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Create Payment Endpoint
@app.post("/payments", response_model=PaymentResponse)
async def create_payment(payment: Payment):
    """Create a new payment document in MongoDB."""
    payment_data = payment.dict()

    # Provide defaults for optional fields if they are None
    if payment_data.get("payee_added_date_utc") is None:
        payment_data["payee_added_date_utc"] = int(datetime.utcnow().timestamp())
    if payment_data.get("payee_due_date") is None:
        payment_data["payee_due_date"] = ""
    if payment_data.get("payee_address_line_1") is None:
        payment_data["payee_address_line_1"] = ""
    if payment_data.get("payee_address_line_2") is None:
        payment_data["payee_address_line_2"] = ""
    if payment_data.get("payee_city") is None:
        payment_data["payee_city"] = ""
    if payment_data.get("payee_country") is None:
        payment_data["payee_country"] = ""
    if payment_data.get("payee_province_or_state") is None:
        payment_data["payee_province_or_state"] = ""
    if payment_data.get("payee_postal_code") is None:
        payment_data["payee_postal_code"] = ""
    if payment_data.get("payee_phone_number") is None:
        payment_data["payee_phone_number"] = ""
    if payment_data.get("payee_email") is None:
        payment_data["payee_email"] = ""
    if payment_data.get("currency") is None:
        payment_data["currency"] = "USD"
    if payment_data.get("discount_percent") is None:
        payment_data["discount_percent"] = 0.0
    if payment_data.get("tax_percent") is None:
        payment_data["tax_percent"] = 0.0

    try:
        result = await payments_collection.insert_one(payment_data)
        created_payment = await payments_collection.find_one({"_id": result.inserted_id})
        if created_payment:
            created_payment["_id"] = str(created_payment["_id"])  # Convert ObjectId to string
            return PaymentResponse(**created_payment)
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve created payment")
    except Exception as e:
        print("Error while adding payment:", e)
        raise HTTPException(status_code=500, detail="Failed to add payment") from e

# Get All Payments Endpoint
@app.get("/payments", response_model=List[PaymentResponse])
async def get_payments():
    """Fetch all payments from MongoDB."""
    try:
        results = await payments_collection.find().to_list(1000)
        payments = []
        for payment in results:
            payment["_id"] = str(payment["_id"])  # Convert ObjectId to string
            payments.append(PaymentResponse(**payment))
        return payments
    except Exception as e:
        print("Error while fetching payments:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch payments") from e

# Get Single Payment by ID Endpoint
@app.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(payment_id: str):
    """Fetch a single payment by its ObjectId."""
    try:
        obj_id = ObjectId(payment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payment ID")

    payment = await payments_collection.find_one({"_id": obj_id})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment["_id"] = str(payment["_id"])  # Convert ObjectId to string
    return PaymentResponse(**payment)

# Update Payment Endpoint
@app.put("/payments/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: str, payment_update: Payment):
    """Update an existing payment (full replacement)."""
    try:
        obj_id = ObjectId(payment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    
    # Prepare update data with defaults
    payment_data = payment_update.dict()
    if payment_data.get("payee_added_date_utc") is None:
        payment_data["payee_added_date_utc"] = int(datetime.utcnow().timestamp())
    if payment_data.get("payee_due_date") is None:
        payment_data["payee_due_date"] = ""
    if payment_data.get("payee_address_line_1") is None:
        payment_data["payee_address_line_1"] = ""
    if payment_data.get("payee_address_line_2") is None:
        payment_data["payee_address_line_2"] = ""
    if payment_data.get("payee_city") is None:
        payment_data["payee_city"] = ""
    if payment_data.get("payee_country") is None:
        payment_data["payee_country"] = ""
    if payment_data.get("payee_province_or_state") is None:
        payment_data["payee_province_or_state"] = ""
    if payment_data.get("payee_postal_code") is None:
        payment_data["payee_postal_code"] = ""
    if payment_data.get("payee_phone_number") is None:
        payment_data["payee_phone_number"] = ""
    if payment_data.get("payee_email") is None:
        payment_data["payee_email"] = ""
    if payment_data.get("currency") is None:
        payment_data["currency"] = "USD"
    if payment_data.get("discount_percent") is None:
        payment_data["discount_percent"] = 0.0
    if payment_data.get("tax_percent") is None:
        payment_data["tax_percent"] = 0.0

    try:
        result = await payments_collection.replace_one(
            {"_id": obj_id},
            payment_data
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found or not modified")
        
        updated_payment = await payments_collection.find_one({"_id": obj_id})
        if updated_payment:
            updated_payment["_id"] = str(updated_payment["_id"])  # Convert ObjectId to string
            return PaymentResponse(**updated_payment)
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve updated payment")
    except Exception as e:
        print("Error while updating payment:", e)
        raise HTTPException(status_code=500, detail="Failed to update payment") from e

# Delete Payment Endpoint
@app.delete("/payments/{payment_id}")
async def delete_payment(payment_id: str):
    """Delete a payment from MongoDB."""
    try:
        obj_id = ObjectId(payment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    result = await payments_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Payment not found or already deleted")
    return {"status": "deleted", "payment_id": payment_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
