# models.py

from pydantic import BaseModel
from typing import Optional, List

class Payment(BaseModel):
    payee_first_name: str
    payee_last_name: str
    due_amount: float
    payee_payment_status: str
    # Optional fields with correct types
    payee_added_date_utc: Optional[int] = None
    payee_due_date: Optional[str] = None
    payee_address_line_1: Optional[str] = None
    payee_address_line_2: Optional[str] = None
    payee_city: Optional[str] = None
    payee_country: Optional[str] = None
    payee_province_or_state: Optional[str] = None
    payee_postal_code: Optional[str] = None
    payee_phone_number: Optional[str] = None
    payee_email: Optional[str] = None
    currency: Optional[str] = "USD"
    discount_percent: Optional[float] = 0.0
    tax_percent: Optional[float] = 0.0

class PaymentResponse(Payment):
    id: str
    payee_added_date_utc: int  # Make this required to ensure consistent sorting

class PaymentsResponse(BaseModel):
    payments: List[PaymentResponse]
    totalPages: int
    currentPage: int
