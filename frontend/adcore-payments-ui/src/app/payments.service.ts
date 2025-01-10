// payments.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface Payment {
  id?: string;
  payee_first_name: string;
  payee_last_name: string;
  due_amount: number;
  payee_payment_status: string;
  payee_added_date_utc?: number;
  payee_due_date?: string;
  payee_address_line_1?: string;
  payee_address_line_2?: string;
  payee_city?: string;
  payee_country?: string;
  payee_province_or_state?: string;
  payee_postal_code?: string;
  payee_phone_number?: string;
  payee_email?: string;
  currency?: string;
  discount_percent?: number;
  tax_percent?: number;
}

export interface PaymentsResponse {
  payments: Payment[];
  totalPages: number;
  currentPage: number;
}

@Injectable({
  providedIn: 'root',
})
export class PaymentsService {
  private BASE_URL = environment.apiUrl; // FastAPI URL

  constructor(private http: HttpClient) {}

  getPayments(
    page: number = 1,
    limit: number = 10,
    search: string = '',
    status: string = '',
    sortField: string = '',
    sortOrder: string = 'asc'
  ): Observable<PaymentsResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('limit', limit.toString());

    if (search) {
      params = params.set('search', search);
    }

    if (status) {
      params = params.set('status', status);
    }

    if (sortField) {
      params = params.set('sortField', sortField).set('sortOrder', sortOrder);
    }

    return this.http.get<PaymentsResponse>(`${this.BASE_URL}/payments`, { params });
  }

  createPayment(payment: Partial<Payment>): Observable<Payment> {
    return this.http.post<Payment>(`${this.BASE_URL}/payments`, payment);
  }

  deletePayment(paymentId: string): Observable<any> {
    return this.http.delete(`${this.BASE_URL}/payments/${paymentId}`);
  }

  updatePayment(paymentId: string, payment: Partial<Payment>): Observable<Payment> {
    return this.http.put<Payment>(`${this.BASE_URL}/payments/${paymentId}`, payment);
  }

  getPaymentById(paymentId: string): Observable<Payment> {
    return this.http.get<Payment>(`${this.BASE_URL}/payments/${paymentId}`);
  }
}
