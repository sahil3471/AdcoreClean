from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from models import Payment, PaymentResponse, PaymentsResponse
import os
import requests  # Added import
import threading  # Added import
import time  # Added import

app = FastAPI()

origins = [
    "https://adcorefullstack.netlify.app",
    "https://www.adcorefullstack.netlify.app",
    # Add other origins if necessary
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# Removed the initial synchronous /test-connection endpoint to avoid duplication

# Self-ping function
def keep_alive():
    # Replace below with your actual Render URL
    url = "https://adcoreclean.onrender.com//test-connection"  # <-- Replace with your Render URL
    interval = 15  # seconds

    while True:
        try:
            response = requests.get(url)
            print(f"[Self-Ping] {url} => {response.status_code}")
        except Exception as e:
            print(f"[Self-Ping] Error: {str(e)}")
        time.sleep(interval)

# Start the keep_alive ping in a background thread
def start_keep_alive():
    t = threading.Thread(target=keep_alive, daemon=True)
    t.start()

# Start the self-ping once the app starts
@app.on_event("startup")
def on_startup():
    start_keep_alive()

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["adcore_payments"]
payments_collection = db["payments"]

# Helper function to map MongoDB document to PaymentResponse
def payment_helper(payment: dict) -> dict:
    return {
        "id": str(payment["_id"]),
        "payee_first_name": payment.get("payee_first_name", ""),
        "payee_last_name": payment.get("payee_last_name", ""),
        "due_amount": payment.get("due_amount", 0.0),
        "payee_payment_status": payment.get("payee_payment_status", ""),
        "payee_added_date_utc": payment.get("payee_added_date_utc") or int(datetime.utcnow().timestamp()),
        "payee_due_date": payment.get("payee_due_date", ""),
        "payee_address_line_1": payment.get("payee_address_line_1", ""),
        "payee_address_line_2": payment.get("payee_address_line_2", ""),
        "payee_city": payment.get("payee_city", ""),
        "payee_country": payment.get("payee_country", ""),
        "payee_province_or_state": payment.get("payee_province_or_state", ""),
        "payee_postal_code": payment.get("payee_postal_code", ""),
        "payee_phone_number": payment.get("payee_phone_number", ""),
        "payee_email": payment.get("payee_email", ""),
        "currency": payment.get("currency", "USD"),
        "discount_percent": payment.get("discount_percent", 0.0),
        "tax_percent": payment.get("tax_percent", 0.0),
    }

# Test Connection Endpoint
@app.get("/test-connection")
async def test_connection():
    """Check if MongoDB is reachable by fetching a sample payment."""
    try:
        sample_payment = await payments_collection.find_one()
        if sample_payment:
            return {"status": "connected", "sample_payment": payment_helper(sample_payment)}
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
    payment_data["payee_added_date_utc"] = payment_data.get("payee_added_date_utc") or int(datetime.utcnow().timestamp())
    payment_data["currency"] = payment_data.get("currency") or "USD"
    payment_data["discount_percent"] = payment_data.get("discount_percent") or 0.0
    payment_data["tax_percent"] = payment_data.get("tax_percent") or 0.0
    
    # Ensure all other optional fields are set to empty strings if None
    optional_string_fields = [
        "payee_due_date",
        "payee_address_line_1",
        "payee_address_line_2",
        "payee_city",
        "payee_country",
        "payee_province_or_state",
        "payee_postal_code",
        "payee_phone_number",
        "payee_email",
    ]
    for field in optional_string_fields:
        payment_data[field] = payment_data.get(field) or ""
    
    try:
        result = await payments_collection.insert_one(payment_data)
        created_payment = await payments_collection.find_one({"_id": result.inserted_id})
        if created_payment:
            return PaymentResponse(**payment_helper(created_payment))
        else:
            raise HTTPException(status_code=500, detail="Failed to retrieve created payment")
    except Exception as e:
        print("Error while adding payment:", e)
        raise HTTPException(status_code=500, detail="Failed to add payment") from e

# Get All Payments Endpoint with Pagination, Search, Sorting, and Filtering
@app.get("/payments", response_model=PaymentsResponse)
async def get_payments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    search: Optional[str] = Query(None, description="Search term for first and last name"),
    status: Optional[str] = Query(None, description="Filter by payment status ('pending' or 'overdue')"),
    sortField: Optional[str] = Query(None, description="Field to sort by"),
    sortOrder: Optional[str] = Query("asc", description="Sort order ('asc' or 'desc')")
):
    """Fetch all payments with pagination, search, sorting, and filtering."""
    try:
        query = {}
        if search:
            # Case-insensitive search for first and last names and status
            query["$or"] = [
                {"payee_first_name": {"$regex": search, "$options": "i"}},
                {"payee_last_name": {"$regex": search, "$options": "i"}},
                {"payee_payment_status": {"$regex": search, "$options": "i"}},
            ]
        if status and status.lower() in ["pending", "overdue"]:
            query["payee_payment_status"] = status.lower()
        
        # Define sorting
        sort_options = {
            "payee_first_name": "payee_first_name",
            "payee_last_name": "payee_last_name",
            "due_amount": "due_amount",
            "payee_payment_status": "payee_payment_status"
        }
        sort_field = sort_options.get(sortField, "payee_added_date_utc")  # Default sort by date
        sort_direction = 1 if sortOrder == "asc" else -1
        
        # Calculate skip
        skip = (page - 1) * limit
        
        # Debugging Logs
        print(f"Fetching payments with query: {query}, sort: {sort_field}, direction: {sort_direction}, page: {page}, limit: {limit}")
        
        # Fetch total count
        total_count = await payments_collection.count_documents(query)
        total_pages = (total_count + limit - 1) // limit  # Ceiling division
        
        # Fetch paginated data
        cursor = payments_collection.find(query).sort(sort_field, sort_direction).skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        payments = [PaymentResponse(**payment_helper(payment)) for payment in results]
        
        # More debugging logs
        print(f"Total count: {total_count}, Total pages: {total_pages}")
        print(f"Retrieved {len(payments)} payments.")
        
        return PaymentsResponse(payments=payments, totalPages=total_pages, currentPage=page)
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

    try:
        payment = await payments_collection.find_one({"_id": obj_id})
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return PaymentResponse(**payment_helper(payment))
    except Exception as e:
        print("Error while fetching payment by ID:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch payment") from e

# Update Payment Endpoint
@app.put("/payments/{payment_id}", response_model=PaymentResponse)
async def update_payment(payment_id: str, payment_update: Payment):
    """Update an existing payment (full replacement)."""
    try:
        obj_id = ObjectId(payment_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payment ID")
    
    payment_data = payment_update.dict()
    
    # Provide defaults for optional fields if they are None
    payment_data["payee_added_date_utc"] = payment_data.get("payee_added_date_utc") or int(datetime.utcnow().timestamp())
    payment_data["currency"] = payment_data.get("currency") or "USD"
    payment_data["discount_percent"] = payment_data.get("discount_percent") or 0.0
    payment_data["tax_percent"] = payment_data.get("tax_percent") or 0.0
    
    # Ensure all other optional fields are set to empty strings if None
    optional_string_fields = [
        "payee_due_date",
        "payee_address_line_1",
        "payee_address_line_2",
        "payee_city",
        "payee_country",
        "payee_province_or_state",
        "payee_postal_code",
        "payee_phone_number",
        "payee_email",
    ]
    for field in optional_string_fields:
        payment_data[field] = payment_data.get(field) or ""
    
    try:
        result = await payments_collection.replace_one(
            {"_id": obj_id},
            payment_data
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found or not modified")
        
        updated_payment = await payments_collection.find_one({"_id": obj_id})
        if updated_payment:
            return PaymentResponse(**payment_helper(updated_payment))
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
    
    try:
        result = await payments_collection.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Payment not found or already deleted")
        return {"status": "deleted", "payment_id": payment_id}
    except Exception as e:
        print("Error while deleting payment:", e)
        raise HTTPException(status_code=500, detail="Failed to delete payment") from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
